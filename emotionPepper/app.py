from flask import Flask, render_template, request, Response, url_for
from speechRecognize import *
from gestureDetection import *
from threading import Thread
from dialogue import Dialogue

import argparse
import os
#import qi


flask_app = Flask(__name__)


class TabletApp(object):
    def __init__(self):
        super(TabletApp, self).__init__()

    # PAGES

    ## FIRST PAGE
    @flask_app.route('/')
    def home():
        try:
            dialogue.gaze.terminate()
        except:
            print("gaze detection already closed")
        Thread(target = dialogue.welcome).start()
        return render_template('welcome.html')

    ## WELCOME     
    @flask_app.route('/welcome', methods=['GET', 'POST'])
    def welcome():
        return render_template('welcome.html')

    ## START        
    @flask_app.route('/start', methods=['GET', 'POST'])
    def start():
        if request.method == "POST":
            mode = request.form['mode']
            numQuiz = request.form['numQuiz']
        dialogue.mode = mode
        dialogue.numQuiz = numQuiz	
        Thread(target = dialogue.start).start()
        return render_template('choice2.html', text = "What's your name?", choice1 = "SPEAK", choice2 = "WRITE", choice1_template = '/speak', choice2_template = '/write', get = "name")

    ## SETTINGS
    @flask_app.route('/settings', methods = ['POST','GET'])
    def settings():
        start = request.form['start']
        return render_template('settings.html', text = " SETTINGS", start = start )

    ## KEYBOARD
    @flask_app.route('/write', methods = ['GET', 'POST'])
    def write():
        if request.method == 'POST':
            return render_template('/write.html', quiz = 'TRUE' )  
        return render_template('/write.html')

    ## RECORD
    @flask_app.route('/speak', methods = ['GET', 'POST'])
    def speak():
        get = request.form['get']
        return render_template('/record.html', get = get)

    ## CHOOSE INSTRUCTIONS
    @flask_app.route('/inst', methods=['GET', 'POST'])
    def inst():
        if request.method == "POST":
            username = request.form['uname']
        dialogue.name = str(username)
        TEXT = "Nice to meet you " + username +", do you want to hear the instructions?"
        Thread(target = dialogue.say, args = [TEXT]).start()
        return render_template('/choice2.html', text = TEXT, choice1 = "YES", choice2 = "NO", choice1_template = '/instructions', choice2_template = '/quiz')

    ## INSTRUCTIONS
    @flask_app.route('/instructions', methods=['GET', 'POST'])
    def intructions():
        if request.method == "POST":
            repeat = request.form['repeat']
        mode = dialogue.mode
        if repeat == 'true':
            Thread(target = dialogue.instructions).start()
            return "OK"
        else:
            Thread(target = dialogue.instructions).start()
            return render_template('/instructions.html', mode = mode)

    ## QUIZ MAIN
    @flask_app.route('/quiz', methods=['GET', 'POST'])
    def quiz():	
            if not hasattr(dialogue,'current_number'):
                dialogue.init_quiz()
            max_number = dialogue.numQuiz
            mode = dialogue.mode
            number = dialogue.current_number
            if int(number) <= int(max_number):
                question, emotion = dialogue.get_question(mode)
                dialogue.current_question = question
                Thread(target = dialogue.quiz, args = [number, question, emotion]).start()
                if str(mode) == 'a':
                    return render_template('/quiz2.html', number = number, text = question, mode = mode)
                elif str(mode) == 'b':
                    return render_template('/quiz3.html', number = number, text = question, mode = mode, choice2 = 'HANDS', choice2_template = '/gesture')
            else:
                final_score = dialogue.score
                Thread(target = dialogue.conclusion).start()
                return render_template('/finish.html', mode = mode, score = final_score)

    ## SMILES (write option for case B)
    @flask_app.route('/smiles')
    def smiles():
        return render_template('quiz4.html')

    ## HAND GESTURES
    @flask_app.route('/gesture')
    def gesture():
        dialogue.gaze.terminate()
        return render_template('/video.html')

    ## SOLUTION
    @flask_app.route('/solution', methods =['GET', 'POST'])
    def solution():
        if request.method == 'POST':		
            answer = request.form['uname']
            hands = request.form['hands']   
            if hands == 'true':
                 answer = gesture.fingerTot        	
        else:
            answer = speech.speech2text()
            print(answer)
            if answer == "":
                TEXT = "OH NO! THERE SEEMED TO BE AN ERROR! TRY AGAIN"
                Thread(target = dialogue.say, args = [TEXT]).start()
                number = dialogue.current_number 
                mode = dialogue.mode
                if mode == 'a':
                    return render_template('/quiz2.html', number = number, text = TEXT, mode = mode)
                elif mode == 'b':
                    return render_template('/quiz3.html', number = number, text = TEXT, mode = mode, choice2 = 'HANDS', choice2_template = '/gesture')
        mode = dialogue.mode	
        score = dialogue.get_score(answer)
        if score == 'error':
            TEXT = "OH NO! THERE SEEMED TO BE AN ERROR! TRY AGAIN"
            Thread(target = dialogue.say, args = [TEXT]).start()
            number = dialogue.current_number 
            mode = dialogue.mode
            if mode == 'a':
                    return render_template('/quiz2.html', number = number, text = TEXT, mode = mode)
            elif mode == 'b':
                    return render_template('/quiz3.html', number = number, text = TEXT, mode = mode, choice2 = 'HANDS', choice2_template = '/gesture')
        name = dialogue.name
        correct = dialogue.current_emotion.upper()
        Thread(target = dialogue.solution, args = [score]).start()
        dialogue.current_number += 1
        return render_template('/solution.html', score = score, mode = mode, name = name, correct = correct)
 
    ## CONCLUSION   
    @flask_app.route('/conclusion', methods = ['GET', 'POST'])
    def conclusion():
        if request.method == 'POST':
            likeGame = request.form['likeGame']
            if likeGame == 'yes':
                TEXT = "DO YOU WANT TO PLAY AGAIN ?"
                dialogue.init_quiz()
                Thread(target = dialogue.say, args = [TEXT]).start()
                return render_template('/choice2.html', text = TEXT, choice1 = "YES", choice2 = "NO", choice1_template = '/quiz', choice2_template = '/conclusion', finish = 'true')
            
            else:
                TEXT = "I'M SORRY YOU DIDN'T LIKED IT, NEXT TIME WE WILL TRY A DIFFERENT GAME"
                try:
                    dialogue.gaze.terminate()
                except:
                    print("gaze detection already closed")
                Thread(target = dialogue.say, args = [TEXT]).start()
                return render_template('/byebye.html', text = TEXT)
        else:
            TEXT = "IT'S BEEN AWSOME TO PLAY WITH YOU \n SEE YOU NEXT TIME, BYE BYE !"
            try:
                    dialogue.gaze.terminate()
            except:
                    print("gaze detection already closed")
            Thread(target = dialogue.say, args = [TEXT]).start()
            return render_template('/byebye.html', text = TEXT)

    # UTILS
    ## IDENTIFY NAME
    @flask_app.route('/checkName')
    def checkName():
        text = speech.speech2text()
        check = ""
        name = ""
        if text == "":
            check = "error"
        else:
            name = dialogue.get_name(text)
            if name == "":
                check = "error"
            else:
                TEXT = " IS YOUR NAME " + name + "?"	
        if check == "error":
            choice1, choice2, choice1_template, choice2_template = "SPEAK", "WRITE", '/speak', '/write'
            TEXT = "OH NO! THERE SEEMED TO BE AN ERROR! TRY AGAIN"		
        else:
            choice1, choice2, choice1_template, choice2_template = "YES", "NO", "/inst", "/write"
        Thread(target = dialogue.say, args = [TEXT]).start()	
        return render_template('choice2.html', text = TEXT, choice1 = choice1, choice2 = choice2, choice1_template = choice1_template, choice2_template = choice2_template,name = name, get = 'name')
   
    ## START RECORD 
    @flask_app.route('/record/')
    def record():
        speech.record()
        return (''), 204	
 
    ## STOP RECORD   
    @flask_app.route('/stopRecord/')
    def stopRecord():
        speech.stop()
        return (''), 204

    ## REPEAT INSTRUCTIONS
    @flask_app.route('/repeatInst/')
    def repeatInst():
        Thread(target = dialogue.instructions).start()
        return (''), 204

    ## HAND GESTURES VIDEO
    @flask_app.route('/video_feed')
    def video_feed():
        return Response(gesture.detect(), mimetype = "multipart/x-mixed-replace; boundary = frame")

    def run(self):
        flask_app.run(debug=True)

if __name__=="__main__":  

    dir_=os.path.abspath('.')+'/'
    filenameJson = dir_ + "sentences.jsonl"

    dialogue = Dialogue(filenameJson)
    speech = SpeechRecognition()
    gesture = GestureDetection()

    tablet_app = TabletApp()
    tablet_app.run()
