from disfluency_removal.audio_receiver_remover import remove
import sounddevice as sd
from scipy.io.wavfile import write
from say import say

import speech_recognition as sr

def speach(sec=15):
    filename="current.wav"
    record(filename,sec)
    remove(filename)
    
    print "converting speach to text..."
    text=speach2text('output.wav')
    
    print(text)
    

def record(filename, sec=15):
    fs = 44100  # Sample rate
    seconds = sec  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, myrecording)  # Save as WAV file 
    
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
    
    return text
    