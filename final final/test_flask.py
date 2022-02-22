from flask import Flask, flash, redirect, render_template, request, session, abort, Response
from tablet_speech_recognition import *
from threading import Thread

from dialogue import Dialogue
import argparse
import qi


flask_app = Flask(__name__)


class TabletApp(object):
    def __init__(self):
        super(TabletApp, self).__init__()

    @flask_app.route('/')
    def home():
		#if not session.get('logged_in'):
		#    return render_template('login.html')
		#else:
	Thread(target = dialogue.welcome).start()
        return render_template('welcome.html')
	
    @flask_app.route('/welcome', methods=['GET', 'POST'])
    def welcome():
        return render_template('welcome.html')
    
    @flask_app.route('/start', methods=['GET', 'POST'])
    def start():
	if request.method == "POST":
            mode = request.form['mode']
	Thread(target = dialogue.start, args = [mode]).start()
        return render_template('choice2.html', text = "What's your name?", choice1 = "speak", choice2 = "write",
                               choice1_template = '/speak', choice2_template = '/write')
	
    @flask_app.route('/settings')
    def settings():
        return render_template('settings.html', text = " SETTINGS" )
    
    @flask_app.route('/write', methods = ['GET', 'POST'])
    def write():
	if request.method == 'POST':
		return render_template('write.html', quiz = 'TRUE' )  
        return render_template('write.html')
    
    @flask_app.route('/speak')
    def speak():
        return render_template('choice2.html', text = "Press REC to record, then press STOP to finish recording", choice1 = "REC", choice2 = "STOP", choice1_template = '/rec', choice2_template = '/stop')
    
    @flask_app.route('/inst', methods=['GET', 'POST'])
    def inst():
        if request.method == "POST":
            username = request.form['uname']
	    dialogue.name = str(username)
            TEXT = "Nice to meet you " + username +", do you want to hear the instructions?"
	Thread(target = dialogue.say, args = [TEXT]).start()
        return render_template('/choice2.html', text = TEXT, choice1 = "YES", choice2 = "NO", choice1_template = '/instructions', choice2_template = '/quiz')

    @flask_app.route('/instructions', methods=['GET', 'POST'])
    def intructions():
	if request.method == "POST":
            repeat = request.form['repeat']
	    mode = request.form['mode']
	    if repeat == 'true':
		Thread(target = dialogue.instructions, args = [mode]).start()
		return "OK"
	    else:
		Thread(target = dialogue.instructions, args = [mode]).start()
		return render_template('/instructions.html', mode = mode)

    @flask_app.route('/quiz', methods=['GET', 'POST'])
    def quiz():
	if request.method == "POST":
		mode = request.form['mode']
		max_number = request.form['numQuiz']
		number = dialogue.current_number
		dialogue.current_number += 1
		if int(number) <= int(max_number):
			if int(number) == 1:
				dialogue.init_quiz()
			question, emotion = dialogue.get_question(mode)
			Thread(target = dialogue.quiz, args = [number, mode, question, emotion]).start()
			if str(mode) == 'a':
				return render_template('/quiz2.html', number = number, text = question, mode = mode)
			elif str(mode) == 'b':
				return render_template('/quiz3.html', number = number, text = question, mode = mode)
		else:
			return render_template('/finish.html')
	else:
		print('error, no post return!')

    @flask_app.route('/solution', methods =['GET', 'POST'])
    def solution():
	if request.method == 'POST':
		mode = request.form['mode']
		answer = request.form['uname']	
		score = dialogue.solution(mode, answer)
		name = dialogue.name
		correct = dialogue.current_emotion.upper()
		Thread(target = dialogue.get_score, args = [mode, score]).start()
		return render_template('/solution.html', score = score, mode = mode, name = name, correct = correct)
	

    @flask_app.route('/gesture')
    def gesture():
	#vision.gaze_detect(backgrnd = False)
	#vision.thread_gesture()
	return render_template('/video.html')

    @flask_app.route('/video_feed')
    def video_feed():
	return Response(vision.gen_frames(), mimetype = "multipart/x-mixed-replace; boundary = frame")

    @flask_app.route('/rec')
    def rec():
        speech.record()

    @flask_app.route('/stop')
    def stop():
        self.speech.stop()
        answer = self.speech.speech2text()
	TEXT = 'Did you said' + answer + ' ?'
        return render_template('choice2.html',text = TEXT, choice1 = 'YES', choice2 = 'NO')
    

    def run(self):
        flask_app.run(debug=True)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1', help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

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

    dialogue = Dialogue(pip, pport, filenameJson, session)

    tablet_app = TabletApp()
    tablet_app.run()
