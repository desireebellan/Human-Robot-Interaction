import qi
import argparse
import sys
import time
import os
import json

from utility import *
from speach_recognition import *
from app_animation_pepper import *

from random import seed
from random import randint

seed(1)

emotions = ['happiness', 'sadness', 'anger', 'fear']
emotion_control = PlayEmotionControl(pip, pport)


class Dialogue(object):
    def __init__(self, pip, pport,cathegory,jsonFilename):
            super(Dialogue, self).__init__()
            self.pip = pip
            self.pport = pport
            self.sentence_filename = jsonFilename
            
    def jsonOpen(self):
        with open(self.sentence_filename) as json_file:
            sentences = json.loads(json_file)
        return sentences
    
    def rand_sentence(self):
        
        choice = randint(0,len(self.sentences)-1)
        
        sentence = self.sentences[choice]
        self.sentences.pop(choice)
        
        return sentence['text'], sentence['emotion'], sentence['tag']
            
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
            name = get_name(answer)
            str = " I'm really happy to meet you, " +  name
    
        # Ask if instructions are needed
        str = "Let's play together! Todays game is called 'emotion game'. Do you want to hear the instructions ?"
        say(str)
        
        # wait for answer
        answer = text().lower()
        
        if 'yes' in answer:
            self.instructions()
        
        self.play_game()
        
     
                   
    def instructions(self):
        
        if self.cathegory == 'autistic':
            # give instructions on the game
            str = "I will say a sentence. Then you'll have to tell me which emotion this sentence transmit, between happyness, sadness, anger or surprise. "
            say(str)
        elif self.cathegory == 'neurotypical':
            str = "I will give you an emotion. Then you'll have to tell me a sentence that describe that emotion." 
            say(str)
            str = "The better the sentence, the highest points you will get ! "
            say(str)
           
        str = "Do you want me to repeat the instructions?"
        str(say)
        
        answer = text().lower()
        
        if 'yes' in answer:
            self.instructions()
        else:
            self.play_game()
       
    def play_game(self):
        str = "Let's start!"
        say(str)  
        
        self.sentences = self.jsonOpen()
        self.emotions = emotions
        self.score = 0
        
        for i in range (2):
            
            str = "Question number " + i+1   
            say(str)  
            if self.cathegory == 'autistic':
                
                # save json with sentences
            
                text, result, tag = self.rand_sentence(self.sentences)
                emotion_control.playEmotion(result)
                say(text)
                
                str = "This sentence is : A Happy, B Sad, C Angry, D Fear"
                
                # wait for answer
                answer = text().lower()
                
                if answer == "":
                    # gesture detection
                    # tablet
                    answer = 
                    
                if answer == result or answer == tag:
                    str = "The answer is correct, good job !"
                    emotion_control.playEmotion('happy')                   
                    say(str)

                
                else :
                    str = "The answer seems to be uncorrect "
                    emotion_control.playEmotion('sad')
                    say(str)
                    str = "The correct answer is: " + result
                    
                                        
            elif self.cathegory == 'neurotypical':
                
            
                emotion= self.rand_emotion()
                str = " Try to say a sentence that express " + emotion
                say(str)
                
                # wait for answer
                answer = text().lower()
                
                score = predict_emotion(answer)
                self.score += score
                
                str = "Your score is: " + score
                
                if score >= 7 :
                    str = "Great job!"
                    emotion_control.playEmotion('happy')
                    say(str)
                    
                elif score>= 5 and score<=6:
                    str = "Not bad!"
                    say(str)
                
                else:
                    str = "Oh no! You will do better next time!"
                    emotion_control.playEmotion('sad')
                    say(str)
                    
        self.conclusion()
                   
    def conclusion(self):
        str = "The game is finished"
        say(str)
        
        if self.cathegory == 'autistic':
            str = "You have done a great job!"
            emotion_control.playEmotion('happy')
            say(str)
            
        if self.cathegory == 'neurotypical':
            str = "Your total score is: "+ self.score
            
        str = " Did you like the emotion game?"
        say(str)
        
        #wait for answer
        
        answer = text().lower()
        if 'yes' in answer:
            str = "I'm so happy that you liked it ! To celebrate it, let's dance together ! "
            say(str)
            
            str = "Do you want to play it again?"
            say(str)
            
            answer = text().lower()
            
            if 'yes' in answer:
                self.play_game()
        if 'no' in answer:
            str = "I'm sorry you didn't liked it, next time we will try a different game ! "
        
        str = "Bye bye!"
        say(str)
        
        
if __name__ ==  "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1', help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")
    parser.add_argument("--cathegory", type=str, default="autisic", help="Cathegory of children: autistic or neurotipical" ) 
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    cathegory = args.cathegory
    


    dialogue = Dialogue(pip, pport, cathegory)
    dialogue.start()