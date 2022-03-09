import re
import os
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from scipy.io.wavfile import write

class SpeechRecognition(object):
    def __init__(self,time = 100, filename_in = 'current.wav', filename_out = "current.wav", language = "en-ENG"):
        self.time = time
        self.filename_in = filename_in
        self.filename_out = filename_out
        self.language = language

    def record(self):
        fs = 44100  # Sample rate
        seconds = self.time  # Duration of recording
	
        print("Recording ...")
        self.myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

    def stop(self):
        sd.stop()
       	#sd.wait()  # Wait until recording is finished
        fs = 44100  # Sample rate
        write(self.filename_in, fs, self.myrecording)  # Save as WAV file 

        data, samplerate = sf.read(self.filename_in)
        os.remove(self.filename_in)
        sf.write(self.filename_in, data, samplerate, subtype = 'PCM_16')  
 
    def speech2text(self): 
        # Input: .wav audio file
        # Output: text string
    
        r = sr.Recognizer()
    
        with sr.AudioFile(self.filename_out) as source:
		# listen for the data (load audio to memory)
                r.adjust_for_ambient_noise(source)
                audio_data = r.record(source)
		# recognize (convert from speech to text)
                try:
                     text = r.recognize_google(audio_data,language=self.language)
                except sr.UnknownValueError:
                     text = ""
                except sr.RequestError as e:
                     text = ""
	    
        text = re.sub(r'((\b\w+\b.{1,2}\w+\b)+).+\1',r'\1', text, flags = re.I)
        text = re.sub(r'\b(\w+)(?:\W+\1\b)+', r'\1', text, flags=re.IGNORECASE)
        return text
    
