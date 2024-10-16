from gtts import gTTS
import sounddevice as sd
import soundfile as sf

def assistant_voice(text):
    # Create a gTTS object for Tagalog text
    if text:
        tts = gTTS(text=text, lang='tl')

        # Save the speech to an audio file
        audio_file = "audio/speech.wav"
        tts.save(audio_file)

        # Load the audio data and sample rate from the file
        data, fs = sf.read(audio_file)

        
        print(text)

        sd.play(data, fs)
        sd.wait()
    else: 
        pass
