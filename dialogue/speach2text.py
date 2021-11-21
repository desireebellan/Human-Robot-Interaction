from IPython.display import Audio, Javascript
from scipy.io import wavfile
from pydub import AudioSegment

import speech_recognition as sr

def speach2text(filename, LANGUAGE="en-ENG"): 
    # Input: .wav audio file
    # Output: text string
    
    r = sr.Recognizer()
    
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data,language=LANGUAGE)
        print (text)
    
    return text
    
