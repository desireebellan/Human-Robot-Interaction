import qi
import argparse
import sys
import time
import os
import json
import time


from utility import *
from app_speech_recognition import *
from app_animation_pepper import *
from emotion_recognition.test import *

from random import seed
from random import randint


emotions = ['happiness', 'sadness', 'anger', 'surprise']


class Dialogue(object):
    def __init__(self, pip, pport,cathegory,jsonFilename, session):
            super(Dialogue, self).__init__()
            self.pip = pip
            self.pport = pport
	    self.cathegory = cathegory
            self.sentence_filename = jsonFilename
	    self.session = session
	    self.emotion_control = PlayEmotionController(pip, pport)
	    self.speech2text = SpeechRecognition()

	    if self.cathegory == 'autistic':
		avertgaze = True
	    else:
		avertgaze = False

	    self.vision = Vision(session = self.session , avertgaze = avertgaze)
            
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

    def answer(self):
	text1 = self.speech2text.speech().lower()
	string = "Is this what you said?"
	say(string, self.pip, self.pport)
	say(str(text1), self.pip, self.pport)
	text2 = self.speech2text.speech().lower()
	if 'yes' in text2:
		return text1
	else:
		string = "Please type your answer"
		say(string, self.pip, self.pport)
		text1 = text().lower()
		return text1
          
    def start(self):
        
        # Pepper Introduce himself
	self.emotion_control.reset()
	time.sleep(5)
	self.vision.gaze_detect('start')
	time.sleep(20)
	
        
        str = "Hi i'm Pepper ! What is your name ?"
        say(str, self.pip, self.pport)
        
        # Receive answer
        answer = self.speech2text.speech()
        #answer = text()
        
        if answer == "":            
            #use tablet
            self.verbal = False
        else:       
            self.verbal = True
            # Get name from answer
            name = get_name(answer)
	    if name == "":
		string = "Sorry I didn't get your name, can you please type it?"
		self.name = text()
	    else:
		self.name=name
            string = " I'm really happy to meet you, {}".format(self.name)
	    say(string, self.pip, self.pport)
    
        # Ask if instructions are needed
        str = "Let's play together! Todays game is called 'emotion game'. Do you want to hear the instructions ?"
        say(str, self.pip, self.pport)
        
        # wait for answer
        answer = self.answer()
        
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
        
        answer = self.answer()
        
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
		
		self.vision.gaze_detect('end')
          
                text_emo, result = self.rand_sentence()
                self.emotion_control.playEmotion(result)
                say(str(text_emo), self.pip, self.pport)
		self.emotion_control.reset()
		time.sleep(15)
                
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
                answer = self.answer()
                                  
                if answer == result or answer == str(tag):
                    string = "The answer is correct, good job {} !".format(self.name)
                    self.emotion_control.playEmotion('happy')                   
                    say(string, self.pip, self.pport)
		    self.emotion_control.reset()
		    time.sleep(15)

                
                else :
                    string = "The answer seems to be uncorrect "
                    self.emotion_control.playEmotion('sad')
                    say(string, self.pip, self.pport,wait)
		    time.sleep(4)
                    string = "The correct answer is: {}".format(result)
		    say(string, self.pip, self.pport)
		    self.emotion_control.reset()
		    time.sleep(15)
                    
                                        
            elif self.cathegory == 'neurotypical':
                
            
                emotion= self.rand_emotion()
                string = " Try to say a sentence that express " + emotion
                say(string, self.pip, self.pport)
                
                # wait for answer
                answer = self.answer()
                
                prediction, score = predict_emotion(answer, emotion)
		score = round(score*10,2)
                self.score += score
                
                string = "Your score is: {:.2f}".format(score*100)
		say(string, self.pip, self.pport)
                
                if score >= 7 :
                    string = "Great job, {}!".format(self.name)
                    self.emotion_control.playEmotion('happy')
                    say(string, self.pip, self.pport)
                    
                elif score>= 5 and score<7:
                    string = "Not bad, {}!".format(self.name)
                    say(string, self.pip, self.pport)
                
                else:
                    string = "Oh no! You will do better next time!"
                    self.emotion_control.playEmotion('sad')
                    say(string, self.pip, self.pport)
		    self.emotion_control.reset()
                    
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
	    time.sleep(15)
            
        elif self.cathegory == 'neurotypical':
            str = "Your total score is: {}".format(self.score)
	    say(str, self.pip, self.pport)
	    time.sleep(5)
            
        str = " Did you like the emotion game?"
        say(str, self.pip, self.pport)
        
        #wait for answer
        
        answer = self.answer()
        if 'yes' in answer:
            string = "I'm so happy that you liked it ! To celebrate it, let's dance together ! "
	    self.emotion_control.playEmotion('happy')
	    self.emotion_control.reset()
            say(string, self.pip, self.pport)
	    time.sleep(15)
		
            
            string = "Do you want to play it again?"
            say(string, self.pip, self.pport)
            
            answer1 = self.answer()
            
            if 'yes' in answer1:
                self.play_game()
        elif 'no' in answer:
            string = "I'm sorry you didn't liked it, next time we will try a different game ! "
	    say(str, self.pip, self.pport)
	    time.sleep(5)
	
	string = "It's been awsome to play with you, {}!".format(self.name)
	say(string, self.pip, self.pport)        
        str = "See you next time, bye bye!"
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

    # Start Application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        print("trying to connect to "+str(connection_url)+"\n")
        app = qi.Application(["HRI", "--qi-url=" + connection_url ])
        print("connected to "+str(connection_url)+"\n")
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    
    dir_=os.path.abspath('.')+'/'
    filenameJson = dir_ + "sentences.jsonl"
    app.start()
    session = app.session

    dialogue = Dialogue(pip, pport, cathegory,filenameJson, session)
    dialogue.start()
