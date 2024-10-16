from openai import OpenAI # type: ignore
from os import getenv
from lib.gpt import GPT
from lib.stt import user_voice as u_voice
from lib.tts import assistant_voice as a_voice

bot = GPT(api_key=getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
while True:
    print("\nYou:")
    user = u_voice()
    print(user)
    if user:
        bot.append_chat("user", user)
        response = bot.create_chat(temperature=1,stream=False)
        print("\nAssistant: ")
        assistant = bot.generate_response(response)
        a_voice(assistant)
        
        bot.append_chat("assistant", assistant)
    else: 
        print("Error: Retrying...")