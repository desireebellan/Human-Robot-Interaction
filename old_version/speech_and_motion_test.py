import qi
import argparse
import sys
import time
import os
import math

from naoqi import ALProxy

# Use outside hri docker container
os.environ['PEPPER_IP'] = '127.0.0.1'


jointsNames = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "HipRoll", "HipPitch", "RHand", "LHand"]

#joint limits taken from http://doc.aldebaran.com/2-5/family/pepper_technical/joints_pep.html
jointLimits ={'HeadYaw': (-2.0857, 2.0857),
              'HeadPitch': (-0.7068, 0.6371),
              'LShoulderPitch': (-2.0857, 2.0857),
              'LShoulderRoll': (0.0087, 1.5620),
              'LElbowYaw': (-2.0857, 2.0857),
              'LElbowRoll': (-1.5620, -0.0087),
              'LWristYaw': (-1.8239, 1.8239),
              'RShoulderPitch': (-2.0857, 2.0857),
              'RShoulderRoll': (-1.5620, -0.0087),
              'RElbowYaw': (-2.0857, 2.0857),
              'RElbowRoll': (0.0087,1.5620),
              'RWristYaw': (-1.8239, 1.8239)}



# ============== #
# Happy Gestures #
# ============== #
def playHappyEmotion(robotIP, PORT, text):

	TO_RAD = math.pi/180.0


	headYT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
	headPT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
	LShoulderPT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
	LShoulderRT = [1.0]
	LElbowYT = [7.0]
	LElbowRT = [1.0, 2.0]
	LWristYT = [7.0]
	RShoulderPT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
	RShoulderRT = [1.0]
	RElbowYT = [7.0]
	RElbowRT = [1.0, 2.0]
	RWristYT = [7.0]
	HipRT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
	HipPT = [1.0]
	RHandT = [1.0]
	LHandT = [1.0]


	headYA = [0.0, 20.0*TO_RAD, 20.0*TO_RAD, 0.0, -20.0*TO_RAD, -20.0*TO_RAD, 0.0]
	headPA = [0.0, -20.0*TO_RAD, 20.0*TO_RAD, 0.0, -20.0*TO_RAD, 20.0*TO_RAD, 0.0]
	LShoulderPA = [20.0*TO_RAD, 50.0*TO_RAD, -20.0*TO_RAD, 50.0*TO_RAD, -20.0*TO_RAD, 50.0*TO_RAD, 0.0]
	LShoulderRA = [45.0*TO_RAD]
	LElbowYA = [-100.0*TO_RAD]
	LElbowRA = [0.0, -55.0*TO_RAD]
	LWristYA = [0.0]
	RShoulderPA = [20.0*TO_RAD, 50.0*TO_RAD, 80.0*TO_RAD, -20.0*TO_RAD, 50.0*TO_RAD, -20.0*TO_RAD, 0.0]
	RShoulderRA = [-45.0*TO_RAD]
	RElbowYA = [100.0*TO_RAD]
	RElbowRA = [0.0, 55.0*TO_RAD]
	RWristYA = [0.0]
	HipRA = [0.0, -15.0*TO_RAD, 0.0, 15.0*TO_RAD, 0.0, -15.0*TO_RAD, 0.0, 15.0*TO_RAD, 0.0]
	HipPA = [-0.12*TO_RAD]
	RHandA = [0.0]
	LHandA = [0.0]

	jointTimes = [headYT, headPT, LShoulderPT, LShoulderRT, LElbowYT, LElbowRT,
		          LWristYT, RShoulderPT, RShoulderRT, RElbowYT, RElbowRT, RWristYT, HipRT, HipPT, RHandT, LHandT]

	jointValues = [headYA, headPA, LShoulderPA, LShoulderRA, LElbowYA, LElbowRA,
		           LWristYA, RShoulderPA, RShoulderRA, RElbowYA, RElbowRA, RWristYA, HipRA, HipPA, RHandA, LHandA]
	#jointTimes = [[3.0], [1.0, 3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0]]
	#jointValues = [[0.0], [20.0*TO_RAD, 0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

	# if (jointValues==None):
	#       print 'No joint values.'
	#       sys.exit(0)

	isAbsolute = True

	# Start service
	print "Executing motion..."
	#motion_service  = self.session.service("ALMotion")
	motionProxy = ALProxy("ALMotion", robotIP, PORT)

	#tts_service = self.session.service("ALTextToSpeech")
	ttsProxy = ALProxy("ALTextToSpeech", robotIP, PORT)

	ttsProxy.setLanguage("English")
	ttsProxy.setVolume(1.0)
	ttsProxy.setParameter("speed", 50)

	motionProxy.post.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)
	ttsProxy.say(text)

	print "End motion execution"

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'], help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
	parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")
	parser.add_argument("--emotion", type=str, default="happy", help="Emotion to mimic. One of {'happy', 'sad', 'afraid', 'special'}")

	args = parser.parse_args()
	pip = args.pip
	pport = args.pport
	emotion = args.emotion

	try:
		connection_url = "tcp://" + pip + ":" + str(pport)
		print("trying to connect to "+str(connection_url)+"\n")

		app = qi.Application(["speech-and-motion", "--qi-url=" + connection_url ])
		print("connected to "+str(connection_url)+"\n")

	except RuntimeError:
		print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport)+ "\nPlease check your script arguments. Run with -h option for help.")
		sys.exit(1)
	
	text = "Hi, I'm Pepper! I'm very very very HAPPY, so I'm dancing, dancing, dancing"
	playHappyEmotion(pip, pport, text)

