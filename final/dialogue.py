import qi
import argparse
import sys
import time
import os
import json
import time

from utility import *
#from speach_recognition import *
from app_animation_pepper import *
from emotion_recognition.test import *

from random import seed
from random import randint


emotions = ['happiness', 'sadness', 'anger', 'surprise']


class Dialogue(object):
    def __init__(self, pip, pport,cathegory,jsonFilename):
            super(Dialogue, self).__init__()
            self.pip = pip
            self.pport = pport
	    self.cathegory = cathegory
            self.sentence_filename = jsonFilename
	    self.emotion_control = PlayEmotionController(pip, pport)
            
    def jsonOpen(self):
        with open(self.sentence_filename) as json_file:
            sentences = json.load(json_file)
        return sentences
    
    def rand_sentence(self):
        
        choice = randint(0,len(self.sentences)-1)
        
        sentence = self.sentences[choice]
        self.sentences.pop(choice)
        
        return sentence['text'], sentence['emotion']
            
    def rand_emotion(self):
        choice = randint(0,len(self.emotions)-1)
        emotion = self.emotions[choice]
        self.emotions.pop(choice)
        
        return emotion
          
    def start(self):
        
        # Pepper Introduce himself
        
        str = "Hi i'm Pepper ! What is your name ?"
        say(str, self.pip, self.pport)
        
        # Receive answer
        #answer = speach()
        answer = text()
        
        if answer == "":            
            #use tablet
            self.verbal = False
        else:       
            self.verbal = True
            # Get name from answer
            self.name = get_name(answer)[0]
            str = " I'm really happy to meet you, {}".format(self.name)
	    say(str, self.pip, self.pport)
    
        # Ask if instructions are needed
        str = "Let's play together! Todays game is called 'emotion game'. Do you want to hear the instructions ?"
        say(str, self.pip, self.pport)
        
        # wait for answer
        answer = text().lower()
        
        if 'yes' in answer:
            self.instructions()
        
        self.play_game()
        
     
                   
    def instructions(self):
        
        if self.cathegory == 'autistic':
            # give instructions on the game
            str = "I will say a sentence. Then you'll have to tell me which emotion this sentence transmit, between happyness, sadness, anger or surprise. "
            say(str, self.pip, self.pport)
        elif self.cathegory == 'neurotypical':
            str = "I will give you an emotion. Then you'll have to tell me a sentence that describe that emotion." 
            say(str, self.pip, self.pport)
            str = "The better the sentence, the highest points you will get ! "
            say(str, self.pip, self.pport)
           
        str = "Do you want me to repeat the instructions?"
        say(str, self.pip, self.pport)
        
        answer = text().lower()
        
        if 'yes' in answer:
            self.instructions()
        else:
            self.play_game()
       
    def play_game(self):
        string = "Let's start!"
        say(string, self.pip, self.pport)  
        
        self.sentences = self.jsonOpen()
        self.emotions = emotions
        self.score = 0
	time.sleep(4)
        
        for i in range (2):
            
            string = "Question number {}".format(i+1)   
            say(string, self.pip, self.pport)  
	    time.sleep(2)
            if self.cathegory == 'autistic':
                
                # save json with sentences
            
                text_emo, result = self.rand_sentence()
                self.emotion_control.playEmotion(result)
                say(str(text_emo), self.pip, self.pport)
		self.emotion_control.reset()
		time.sleep(6)
                
                string = "This sentence is : 1 Happy, 2 Sad, 3 Angry, 4 Fear"
		say(string, self.pip, self.pport)
		if result == 'happy':
			tag=1
		elif result == 'sad':
			tag=2
		elif result == 'angry':
			tag=3
		elif result =='fear':
			tag=4
                
                # wait for answer
                answer = text().lower()
                
                if answer == "":
                    # gesture detection
                    # tablet
                    string = " Non verbal mode active "
		    say(string, self.pip, self.pport)
                    
                if answer == result or answer == str(tag):
                    string = "The answer is correct, good job !"
                    self.emotion_control.playEmotion('happy')                   
                    say(string, self.pip, self.pport)
		    self.emotion_control.reset()
		    time.sleep(10)

                
                else :
                    string = "The answer seems to be uncorrect "
                    self.emotion_control.playEmotion('sad')
                    say(string, self.pip, self.pport,wait)
		    time.sleep(4)
                    string = "The correct answer is: {}".format(result)
		    say(string, self.pip, self.pport)
		    self.emotion_control.reset()
		    time.sleep(4)
                    
                                        
            elif self.cathegory == 'neurotypical':
                
            
                emotion= self.rand_emotion()
                string = " Try to say a sentence that express " + emotion
                say(string, self.pip, self.pport)
                
                # wait for answer
                answer = text().lower()
                
                prediction, score = predict_emotion(answer, emotion)
		score = round(score*100,2)
                self.score += score
                
                string = "Your score is: {:.2f}".format(score*100)
		say(string, self.pip, self.pport)
                
                if score >= 7 :
                    string = "Great job!"
                    self.emotion_control.playEmotion('happy')
                    say(string, self.pip, self.pport)
                    
                elif score>= 5 and score<7:
                    string = "Not bad!"
                    say(string, self.pip, self.pport)
                
                else:
                    string = "Oh no! You will do better next time!"
                    self.emotion_control.playEmotion('sad')
                    say(string, self.pip, self.pport)
                    
        self.conclusion()
                   
    def conclusion(self):
        str = "The game is finished"
        say(str, self.pip, self.pport)
	time.sleep(5)
        
        if self.cathegory == 'autistic':
            str = "You have done a great job!"
            self.emotion_control.playEmotion('happy')
	    self.emotion_control.reset()
            say(str, self.pip, self.pport)
	    time.sleep(5)
            
        if self.cathegory == 'neurotypical':
            str = "Your total score is: {}".format(self.score)
	    say(str, self.pip, self.pport)
	    time.sleep(5)
            
        str = " Did you like the emotion game?"
        say(str, self.pip, self.pport)
        
        #wait for answer
        
        answer = text().lower()
        if 'yes' in answer:
            str = "I'm so happy that you liked it ! To celebrate it, let's dance together ! "
	    emotion_control.playEmotion('happy')
	    self.emotion_control.reset()
            say(str, self.pip, self.pport)
	    time.sleep(10)
		
            
            str = "Do you want to play it again?"
            say(str, self.pip, self.pport)
            
            answer = text().lower()
            
            if 'yes' in answer:
                self.play_game()
        if 'no' in answer:
            str = "I'm sorry you didn't liked it, next time we will try a different game ! "
	    say(str, self.pip, self.pport)
	    time.sleep(5)
        
        str = "Bye bye!"
        say(str, self.pip, self.pport)
        
        
if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1', help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")
    parser.add_argument("--cathegory", type=str, default="autistic", help="Cathegory of children: autistic or neurotipical" ) 
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    cathegory = args.cathegory
    
    dir_=os.path.abspath('.')+'/'
    filenameJson = dir_ + "sentences.jsonl"

    dialogue = Dialogue(pip, pport, cathegory,filenameJson)
    dialogue.start()
