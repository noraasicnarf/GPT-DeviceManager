from openai import OpenAI
import json
from lib.comm import send_command
class GPT():
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.messages = [
            {"role": "system", "content": """
             - You are a helpful assistant named "Eva".
             - Your only task is to assist about turning off and on devices (fan,light)
             - Ask the user to confirm turning on/off devices, if users mentioned a context that is related to devices such as (Lightings, Darkness, Temparature, Humidity)
             """},# You can improve the system instruction based on your needs
        ]
        self.tools = [
                    {
                      "type": "function",
                      "function": {
                        "name": "send_device_command",
                        "description": "Could be based from a condition when to use. Also for user direct commands to turn on/off light and fan", #Modify description
                        "parameters": {
                          "type": "object",
                          "required": [
                            "device_commands"
                          ],
                          "properties": {
                            "device_commands": {
                              "type": "array",
                              "description": "List of commands to control devices",
                              "items": {
                                "type": "object",
                                "required": [
                                  "device",
                                  "action"
                                ],
                                "properties": {
                                  "device": {
                                    "type": "string",
                                    "description": "Device to control (fan, light)", #Modify description
                                    "enum": [
                                      "fan",
                                      "light",
                                      #Add your devices here
                                    ]
                                  },
                                  "action": {
                                    "type": "string",
                                    "description": "Action to perform on the device (turn_on, turn_off)",
                                    "enum": [
                                      "turn_on",
                                      "turn_off"
                                    ]
                                  },
                                },
                                "additionalProperties": False
                              }
                            }
                          },
                          "additionalProperties": False
                        },
                        "strict": True
                      }
                    }
                  ]
    # initializes chat completion
    def create_chat(self, temperature: float, seed: int = None, stream: bool = False):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
            seed=seed,
            stream=stream,                     
            tools = self.tools,
            parallel_tool_calls =  False,
            response_format =  {
              "type": "text"
            }
                  )
        return response
    # Appends user or assistant to messages
    def append_chat(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    # Function calling process
    def tool_call(self, chat):
    # Extract tool call details
      tools = chat.choices[0].message.tool_calls[0]
      call_id = tools.id
      name = tools.function.name
      arguments = json.loads(tools.function.arguments)
      
      # Get device commands
      commands = arguments['device_commands']

      tool_message = {
          "role": "assistant",
          "content": [
              { "type": "text", "text": "" }
          ],
          "tool_calls": [
              {
                  "id": call_id,
                  "type": "function",
                  "function": {
                      "name": name,
                      "arguments": "Explain per device: " + json.dumps(arguments)
                  }
              }
          ]
      }

      self.messages.append(tool_message) # Append the second message with tool call results
    

      #send command to arduino
      result = send_command(commands)
      
      #append tool result
      self.messages.append({
          "role": "tool",
          "content": [
              {
                  "type": "text",
                  "text": json.dumps(result)
              }
          ],
          "tool_call_id": call_id
      })
    
    # Generate unstreamed response
    def generate_response(self, chat):
        if chat.choices[0].message.tool_calls is not None: # tool calls
            self.tool_call(chat)
            #create response with tool return
            chat = self.create_chat(temperature=1)
            return chat.choices[0].message.content
        else:
            return chat.choices[0].message.content
    # Generate streamed response, tool_call not complete yet
    def generate_stream(self, chat):
        buffer = []  # Use list comprehension to filter out None values

        for chunk in chat:
             message_chunk = chunk.choices[0].delta.content
             tools = chunk.choices[0].delta.tool_calls
             if tools is not None:
                 print(tools)
             if message_chunk is not None:
                 print(message_chunk, end='')
                 buffer.append(message_chunk)
        stream = ''.join(buffer)
        return stream  # Return the final string
