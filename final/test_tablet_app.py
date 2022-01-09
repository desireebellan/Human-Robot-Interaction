from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import argparse

import qi
import argparse
import sys
import time

from app_animation_pepper import PlayEmotionController
from dialogue import Dialogue
from naoqi import ALProxy

flask_app = Flask(__name__)

#correctUserName = ''

# pip = '127.0.0.1'
# pport = 9559

"""
emotion_control = PlayEmotionController(pip, pport)

def say(text, pip, pport):
	ttsProxy = ALProxy("ALTextToSpeech", pip, pport)
	ttsProxy.setLanguage("English")
	ttsProxy.setVolume(1.0)
	ttsProxy.setParameter("speed", 50)
	ttsProxy.say(text)

class PepperAction(object):
	def __init__(self, pip, pport):
		super(PepperAction, self).__init__()

		self.pip = pip
		self.pport = pport

	def talk(self):
		# TEST CONNECTION #
		strans = 'Francesco'
		say("Ciao, mi chiamo Pepper!, Come ti chiami?", self.pip, self.pport)
		return strans
"""

dialogue = None

class TabletApp(object):
	def __init__(self, pip, pport, cathegory,filenameJson, session):
		super(TabletApp, self).__init__()
		self.pip = pip
		self.pport = pport
		self.cathegory = cathegory
		self.filenameJson = filenameJson
		self.session = session

	answer_tablet = ""
	correctUserName = ""

	@flask_app.route('/')
	def home():
		#if not session.get('logged_in'):
		#    return render_template('login.html')
		#else:
		return render_template('welcome.html')

	"""
	@app.route('/login', methods=['POST'])
	def do_admin_login():
		if request.form['password'] == 'secret' and request.form['username'] == 'admin':
		    session['logged_in'] = True
		else:
		    flash('wrong password!')
		return home()

	@app.route("/logout")
	def logout():
		session['logged_in'] = False
		return home()
	"""

	@flask_app.route('/welcome')
	def welcome():
		return render_template('welcome.html')

	@flask_app.route('/start')#, methods=['GET', 'POST'])
	def start():
		dialogue.start()

		return render_template('start.html')#, userName = answer)

	@flask_app.route('/record')
	def record():
		print 'I got clicked!'

	@flask_app.route('/insts', methods=['GET', 'POST'])
	def insts():

		if request.method == "POST":
			# getting input with name = fname in HTML form
			correctUserName = request.form.get("uname")
			print "Your (correct) name is "+ correctUserName

		return render_template('insts.html', userName = correctUserName)

	@flask_app.route('/quiz', methods=['GET', 'POST'])
	def quiz():

		# Generate question
		text_emo = "Today we had a lot of fun together"
		result = "happy"
		#emotion_control.playEmotion(result)

		say(str(text_emo), pip, pport)

		#time.sleep(5)

		string = "This sentence is : 1 Happy, 2 Sad, 3 Angry, 4 Fear"
		say(string, pip, pport)

		if result == 'happy':
			tag=1
		elif result == 'sad':
			tag=2
		elif result == 'angry':
			tag=3
		elif result =='fear':
			tag=4

		"""

		if request.method == "POST":
			# wait for answer
			answer_speech = "happy"
			answer_tablet = request.form.get("uname")
			print "\n#### Answer from tablet: {} ####\n".format(answer_tablet)

			if answer == result or answer == str(tag):
				string = "The answer is correct, good job {} !".format(correctName)
				emotion_control.playEmotion('happy')                   
				say(string, pip, pport)
				emotion_control.reset()
				time.sleep(15)

				
			else :
				string = "The answer seems to be uncorrect "
				emotion_control.playEmotion('sad')
				say(string, pip, pport)
				time.sleep(4)
				string = "The correct answer is: {}".format(result)
				say(string, pip, pport)
				emotion_control.reset()
				time.sleep(15)
		"""

		return render_template('quiz.html', sentence=str(text_emo), answer=str(result), tag=str(tag))

	def run(self):
		flask_app.run(debug=True)

if __name__=='__main__':
	# parse input arguments
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

	# create Dialogue object
	dialogue = Dialogue(pip, pport, cathegory,filenameJson, session)
	# create Tablet_App object
	tablet_app = TabletApp(pip, pport, cathegory,filenameJson, session)

	# start tablet app
	tablet_app.run()
