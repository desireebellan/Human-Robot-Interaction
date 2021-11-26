from disfluency_removal.audio_receiver_remover import remove_dis
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr


class SpeachRecognition(object):
    def __init__(self,time = 15, filename_in = "current.wav", filename_out = "output.wav", language = "en-ENG"):
        self.time = time
        self.filename_in = filename_in
        self.filename_out = filename_out
        self.language = language

    def speach(self):
        self.record()
        remove_dis(self.filename_in, self.filename_out)
    
        print "converting speach to text..."
        text = self.speach2text()
    
        print(text)
    

    def record(self):
        fs = 44100  # Sample rate
        seconds = self.time  # Duration of recording

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write(self.filename_in, fs, myrecording)  # Save as WAV file 
    
    def speach2text(self): 
        # Input: .wav audio file
        # Output: text string
    
        r = sr.Recognizer()
    
        with sr.AudioFile(self.filename_out) as source:
            # listen for the data (load audio to memory)
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data,language=self.language)
    
        return text
    