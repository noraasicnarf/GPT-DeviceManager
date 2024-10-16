import vosk
import pyaudio
import json

# Initialize the Vosk model (adjust the model path as needed)
model = vosk.Model("vosk-model-tl-ph-generic-0.6")

# Create a recognizer using the Vosk model
rec = vosk.KaldiRecognizer(model, 16000)

# PyAudio setup
p = pyaudio.PyAudio()

# Function to capture and process user's voice
def user_voice():
    # Open an audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4096)

    
    while True:
        # Read the audio input in chunks
        data = stream.read(4096)
        
        # Check if Vosk recognized the speech input
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            recognized_text = result.get('text', '')
            
            # Check if any text was recognized
            if recognized_text:
                
                # If the user says "terminate", end the voice capture
                if "terminate" in recognized_text.lower():
                    break
                
                return recognized_text
            

    # Stop the stream after the loop
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Return empty string if no text was recognized
    return ""
