import argparse
import sys
import time
import os
import json
import time
import subprocess

from emotion_recognition.test import *
from random import randint

import nltk
nltk.download('punkt')

#to download correctly nltk.tag.stanford.StenfordNERTagger
# change the java_path to the path on you computer

java_path = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java.exe"
os.environ['JAVAHOME'] = java_path

from nltk.tag.stanford import StanfordNERTagger


dir_=os.path.abspath('.')+'/'
st = StanfordNERTagger(dir_+'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', dir_+'stanford-ner/stanford-ner.jar')


emotions = ['happiness', 'sadness', 'anger', 'surprise']


class Dialogue(object):
    def __init__(self, jsonFilename):
        super(Dialogue, self).__init__()

        self.sentence_filename = jsonFilename
        self.mode = 'a'

    # MAIN FUNCTIONS (called by app.py)
    ## WELCOME
    def welcome(self):
        self.name = ""
        self.numQuiz = 2
        text = "Hi i'm Pepper ! Welcome to the Emotion Game !"
        p = subprocess.Popen(["python2","speechMotion.py", "--text", text, "--emotion", "reset"], stdout = subprocess.PIPE)
        p.wait()
    ## START  
    def start(self):
        # Pepper Introduce himself
        if self.mode == 'a':
            self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(False)], stdout = subprocess.PIPE)
        if self.mode == 'b':
            self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(True)], stdout = subprocess.PIPE)
        text = "What's your name?"
        p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
        p.wait()
             
    
    def say(self, text):
        text = str(text)
        p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
        p.wait()

    ## INSTRUCTIONS                 
    def instructions(self):
        
        if self.mode == 'b':
            # give instructions on the game
            text = "I will say a sentence. Then you'll have to tell me which emotion this sentence transmit, between happyness, sadness, anger or surprise. "
            p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
            p.wait()
        elif self.mode == 'a':
            text = "I will give you an emotion. Then you'll have to tell me a sentence that describe that emotion." 
            p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
            p.wait()
            text = "The better the sentence, the highest points you will get ! "
            p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
            p.wait()
        text = "Do you want me to repeat the instructions?"
        p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
        p.wait()
 
    ## INITIALIZE QUIZ  
    def init_quiz(self):
        self.sentences = self.jsonOpen()
        self.emotions = emotions 
        self.score = 0  
        self.current_question = ""
        self.current_emotion = ""
        self.current_number = 1

    ## GET QUIZ QUESTIONS
    def get_question(self, mode):
        if mode == 'a':
            self.current_emotion = self.rand_emotion()
            return "Try to say a sentence that express " +  self.current_emotion , self.current_emotion
        else:
            sentence, self.current_emotion = self.rand_sentence()
            return sentence, self.current_emotion

    ## QUIZ
    def quiz(self, number, question, emotion): 
        self.current_emotion = emotion
        text = "Question number {}".format(int(number))   
        subprocess.run(["python2","speechMotion.py", "--text", text])
        if self.mode == 'b':	
            self.gaze.terminate()
            subprocess.run(["python2","speechMotion.py", "--text", question, "--emotion", emotion])
            subprocess.run(["python2","speechMotion.py","--emotion", "reset"])
            text = "This sentence is : 1 Happy, 2 Sad, 3 Angry, 4 Fear"
            subprocess.run(["python2","speechMotion.py", "--text", text])
            self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(True)], stdout = subprocess.PIPE)
        elif self.mode == 'a':
            self.gaze.terminate()
            p = subprocess.Popen(["python2","speechMotion.py", "--text", question, "--emotion", emotion], stdout = subprocess.PIPE)
            out, err = p.communicate()
            p.wait()
            print(out)          
            p = subprocess.Popen(["python2","speechMotion.py","--emotion", 'reset'], stdout = subprocess.PIPE)
            out, err = p.communicate()
            p.wait()
            print(out)
            self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(False)], stdout = subprocess.PIPE)

    ## GET SCORE
    def get_score(self, answer):
        if str(self.mode) == 'a':
            print(answer)
            score = predict_emotion(str(answer), self.current_emotion)
            score = round(score*10,2)
            self.score += score
                       
        elif str(self.mode) == 'b':
            print(answer)
            if self.current_emotion == 'happy':
               tag = 1
            elif self.current_emotion == 'sad':
                tag = 2
            elif self.current_emotion == 'angry':
                tag = 3
            elif self.current_emotion =='fear':
                tag = 4
            if type(answer) == str:
                emotions = ['happy', 'sad', 'fear', 'angry']
                numbers = ['1','2','3','4']
                check_emotion = [True if emotion in answer.lower() else False for emotion in emotions]
                check_number = [True if str(emotion) in answer.lower() else False for emotion in numbers]
                if any(check_emotion) or any(check_number):
                    if self.current_emotion in answer.lower() or str(tag) in answer.lower():
                        score = 1;
                                  
                    else :
                        score = 0;
                else:
                    score = "error"
            else:
                if answer == 0:
                    score = "error"
                elif answer == tag:
                    score = 1;
                else:
                    score = 0;
        return score

    ## SOLUTION
    def solution(self, score):
        if self.gaze:
            self.gaze.terminate()
        if self.mode == 'a':
            text = "Your score is: {:.2f}".format(score)
            p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
            p.wait()

            if score >= 7 :
                    text = "Great job, {}!".format(self.name)
                    p = subprocess.Popen(["python2","speechMotion.py", "--text", text, "--emotion", 'happy'], stdout = subprocess.PIPE)
                    p.wait()
                    
            elif score>= 5 and score<7:
                    text = "Not bad, {}!".format(self.name)
                    p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
                    p.wait()
                
            else:
                    text = "Oh no! You will do better next time!"
                    p = subprocess.Popen(["python2","speechMotion.py", "--text", text, "--emotion", 'sad'], stdout = subprocess.PIPE)
                    p.wait()
            p = subprocess.Popen(["python2","speechMotion.py","--emotion", 'reset'], stdout = subprocess.PIPE)
            p.wait()
            self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(False)], stdout = subprocess.PIPE)

        if self.mode == 'b':
            if score == 1:
                text = "The answer is correct, good job {} !".format(self.name)
                p = subprocess.Popen(["python2","speechMotion.py", "--text", text, "--emotion", 'happy'], stdout = subprocess.PIPE)
                p.wait()
                p = subprocess.Popen(["python2","speechMotion.py","--emotion", 'reset'], stdout = subprocess.PIPE)
                p.wait()
            else:
                text = "The answer seems to be uncorrect "
                p = subprocess.Popen(["python2","speechMotion.py", "--text", text, "--emotion", 'reset'], stdout = subprocess.PIPE)
                p.wait()
                text = "The correct answer is: {}".format(self.current_emotion)
                p = subprocess.Popen(["python2","speechMotion.py", "--text", text, "--emotion", 'reset'], stdout = subprocess.PIPE)
                p.wait()
                self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(True)], stdout = subprocess.PIPE)
            
    ## CONCLUSION               
    def conclusion(self):
        text = "The game is finished"
        p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
        p.wait()
        self.gaze.terminate()
        if self.mode == 'b':
            text = "You have done a great job!"
            p = subprocess.Popen(["python2","speechMotion.py", "--text", text, "--emotion", 'happy'], stdout = subprocess.PIPE)
            p.wait()
            p = subprocess.Popen(["python2","speechMotion.py","--emotion", 'reset'], stdout = subprocess.PIPE)
            p.wait()
            self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(True)], stdout = subprocess.PIPE)
            
        elif self.mode == 'a':
            text = "Your final score is: {}".format(self.score)
            p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
            p.wait()
            self.gaze = subprocess.Popen(["python2","gazeDetect.py", "--avertgaze", str(False)], stdout = subprocess.PIPE)
            
        text = " Did you like the emotion game?"
        p = subprocess.Popen(["python2","speechMotion.py", "--text", text], stdout = subprocess.PIPE)
        p.wait()

    # UTILS
    ## GET NAME
    def get_name(self,textin):
         name =""
         for sent in nltk.sent_tokenize(textin):
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = st.tag(tokens)
            for tag in tags:
                if tag[1]=='PERSON': 
                     name = tag[0]	
         return name
       
    ## OPEN JSON FILE        
    def jsonOpen(self):
        with open(self.sentence_filename) as json_file:
            sentences = json.load(json_file)
        return sentences
    
    ## SELECT RANDOM SENTENCE-EMOTION PAIR
    def rand_sentence(self):
        
        choice = randint(0,len(self.sentences)-1)
        
        sentence = self.sentences[choice]
        self.sentences.pop(choice)
        
        return sentence['text'], sentence['emotion']
      
    ## SELECT RANDOM EMOTION      
    def rand_emotion(self):
        choice = randint(0,len(self.emotions)-1)
        emotion = self.emotions[choice]
        
        return emotion


    
    
        
        

