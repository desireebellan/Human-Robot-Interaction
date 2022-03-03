import qi
import argparse
import sys
import time
import os
import math


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


class PlayEmotionController(object):
	def __init__(self, app):
		super(PlayEmotionController, self).__init__()

		app.start()
		self.session = app.session


	# ============ #
	# Sad Gestures #
	# ============ #
	def playSadEmotion(self, joint_values = None):

    		TO_RAD = math.pi/180.0


		headYT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
		headPT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
		LShoulderPT = [3.0]
		LShoulderRT = [1.0, 3.0]
		LElbowYT = [1.0, 3.0]
		LElbowRT = [3.0]
		LWristYT = [3.0, 4.0, 5.0, 6.0, 7.0]
		RShoulderPT = [3.0]
		RShoulderRT = [1.0, 3.0]
		RElbowYT = [1.0, 3.0]
		RElbowRT = [5.0]
		RWristYT = [3.0, 4.0, 5.0, 6.0, 7.0]
		HipRT = [3.0]
                HipPT = [3.0,5.0,6.0,8.0]
                RHandT = [1.0, 8.0]
                LHandT = [1.0, 8.0]

		headYA = [0.0, 0.0, 0.0, -20.0*TO_RAD, 20.0*TO_RAD, -20.0*TO_RAD, 20.0*TO_RAD, 0.0]
		headPA = [10.0*TO_RAD, 30.0*TO_RAD, 30.0*TO_RAD, 30.0*TO_RAD, 30.0*TO_RAD, 30.0*TO_RAD, 30.0*TO_RAD, 5.0*TO_RAD]
		LShoulderPA = [0.0*TO_RAD]
		LShoulderRA = [0.0, 25.0*TO_RAD]
		LElbowYA = [-100.0*TO_RAD, -50.0*TO_RAD]
		LElbowRA = [-89.0*TO_RAD]
		LWristYA = [0.0, -25.0*TO_RAD, 25.0*TO_RAD, -25.0*TO_RAD, 0.0]
		RShoulderPA = [0.0*TO_RAD]
		RShoulderRA = [0.0, -25.0*TO_RAD]
		RElbowYA = [100.0*TO_RAD, 50.0*TO_RAD]
		RElbowRA = [85.0*TO_RAD]
		RWristYA = [0.0, -25.0*TO_RAD, 25.0*TO_RAD, -25.0*TO_RAD, 0.0]
		HipRA = [0.0]
                HipPA = [-20*TO_RAD, -40.0*TO_RAD, -40.0*TO_RAD, -7.0*TO_RAD]
                RHandA = [-100.0*TO_RAD, -100.0*TO_RAD]
                LHandA = [-100.0*TO_RAD, -100.0*TO_RAD]

		jointTimes = [headYT, headPT, LShoulderPT, LShoulderRT, LElbowYT, LElbowRT,
                              LWristYT, RShoulderPT, RShoulderRT, RElbowYT, RElbowRT, RWristYT, HipRT, HipPT, RHandT, LHandT]

		jointValues = [headYA, headPA, LShoulderPA, LShoulderRA, LElbowYA, LElbowRA,
                               LWristYA, RShoulderPA, RShoulderRA, RElbowYA, RElbowRA, RWristYA, HipRA, HipPA, RHandA, LHandA]

                #jointTimes = [[3.0], [1.0, 3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0]]
                #jointValues = [[0.0], [20.0*TO_RAD, 0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

                # if (jointValues==None):
		# 	print 'No joint values.'
		#       sys.exit(0)

		isAbsolute = True

		# Start service
		print "Executing motion..."
		motion_service  = self.session.service("ALMotion")
		motion_service.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)
		print "End motion execution"



	# ============== #
        # Happy Gestures #
        # ============== #
	def playHappyEmotion(self, joint_values = None):

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
                motion_service  = self.session.service("ALMotion")
                motion_service.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)
                print "End motion execution"


	# =============== #
	# Afraid Gestures #
	# =============== #
	def playAfraidEmotion(self, joint_values = None):

                TO_RAD = math.pi/180.0


                headYT = [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
                headPT = [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
                LShoulderPT = [3.0]
                LShoulderRT = [3.0]
                LElbowYT = [8.0, 9.0]
                LElbowRT = [8.0, 9.0]
                LWristYT = [8.0, 9.0]
                RShoulderPT = [3.0]
                RShoulderRT = [3.0]
                RElbowYT = [8.0, 9.0]
                RElbowRT = [8.0, 9.0]
                RWristYT = [8.0, 9.0]
                HipRT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
                HipPT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
                RHandT = [1.0]
                LHandT = [1.0]


                headYA = [0.0, 0.0, 0.0, 0.0, 40.0*TO_RAD, 0.0, -40.0*TO_RAD, 0.0]
                headPA = [0.0, 20.0*TO_RAD, 0.0, 0.0, 0.0, 0.0, 0.0, 20.0*TO_RAD]
                LShoulderPA = [0.0]
                LShoulderRA = [0.0]
                LElbowYA = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -50.0*TO_RAD]
                LElbowRA = [0.0, -65.0*TO_RAD]
                LWristYA = [-100.0*TO_RAD, -100.0*TO_RAD]
                RShoulderPA = [0.0]
                RShoulderRA = [0.0]
                RElbowYA = [0.0, 50.0*TO_RAD]
                RElbowRA = [0.0, 65.0*TO_RAD]
                RWristYA = [100.0*TO_RAD, 100.0*TO_RAD]
                HipRA = [-20.0*TO_RAD, -40.0*TO_RAD, -20.0*TO_RAD, 0.0, 20.0*TO_RAD, 40.0*TO_RAD, 20.0*TO_RAD, 0.0]
                HipPA = [10.0*TO_RAD, 30.0*TO_RAD, 10.0*TO_RAD, 0.0, 10.0*TO_RAD, 30.0*TO_RAD, 10.0*TO_RAD, 0.0]
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
		motion_service = self.session.service("ALMotion")

                motion_service.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)
		#self.circle(0.5, motion_service2)
		#self.test_speed(motion_service2)

                print "End motion execution"



        # =============== #
        # Angry Gestures  #
        # =============== #
        def playAngryEmotion(self, joint_values = None):

                TO_RAD = math.pi/180.0

                headYT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
                headPT = [1.0, 3.0, 4.0, 7.0]
                LShoulderPT = [3.0, 4.0, 7.0, 12.0]
                LShoulderRT = [3.0, 5.0, 7.0]
                LElbowYT = [3.0]
                LElbowRT = [1.0, 3.0, 5.0]
                LWristYT = [3.0]
                RShoulderPT = [3.0, 4.0, 7.0, 12.0]
                RShoulderRT = [3.0, 5.0, 7.0]
                RElbowYT = [3.0]
                RElbowRT = [1.0, 3.0, 5.0]
                RWristYT = [3.0]
                HipRT = [1.0, 3.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
                HipPT = [1.0]
                RHandT = [1.0]
                LHandT = [1.0]


                headYA = [0.0, 0.0, 0.0, -20.0*TO_RAD, 20.0*TO_RAD, -20.0*TO_RAD, 20.0*TO_RAD, 0.0]
                headPA = [0.0, 0.0, 10.0*TO_RAD, 10.0*TO_RAD]
                LShoulderPA = [10.0*TO_RAD, 10.0*TO_RAD, 91.0*TO_RAD, 91.0*TO_RAD]
                LShoulderRA = [0.0, 0.0, 50.0*TO_RAD]
                LElbowYA = [-20.0*TO_RAD]
                LElbowRA = [0.0, -85.0*TO_RAD, -85.0*TO_RAD]
                LWristYA = [20.0*TO_RAD]
                RShoulderPA = [10.0*TO_RAD, 10.0*TO_RAD, 91.0*TO_RAD, 91.0*TO_RAD]
                RShoulderRA = [0.0, 0.0, -50.0*TO_RAD]
                RElbowYA = [0.0]
                RElbowRA = [0.0, 85.0*TO_RAD, 85.0*TO_RAD]
                RWristYA = [-20.0*TO_RAD]
                HipRA = [0.0, 0.0, 0.0, -10.0*TO_RAD, 10.0*TO_RAD, -10.0*TO_RAD, 10.0*TO_RAD, 0.0]
                HipPA = [-0.12*TO_RAD]
                RHandA = [0.0]
                LHandA = [0.0]

                jointTimes = [headYT, headPT, LShoulderPT, LShoulderRT, LElbowYT, LElbowRT,
                              LWristYT, RShoulderPT, RShoulderRT, RElbowYT, RElbowRT, RWristYT, HipRT, HipPT, RHandT, LHandT]

                jointValues = [headYA, headPA, LShoulderPA, LShoulderRA, LElbowYA, LElbowRA,
                               LWristYA, RShoulderPA, RShoulderRA, RElbowYA, RElbowRA, RWristYA, HipRA, HipPA, RHandA, LHandA]

                # if (jointValues==None):
                #       print 'No joint values.'
                #       sys.exit(0)

                isAbsolute = True

                # Start service
                print "Executing motion..."
                motion_service = self.session.service("ALMotion")

                motion_service.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)
                #self.circle(0.5, motion_service2)
                #self.test_speed(motion_service2)

                print "End motion execution"



	def test_speed(self, motion_service):
		theta = math.pi/4
		v = 0.3
		distance = 0.0

		i=1
		while distance <= 2*math.pi:
			theta = theta*(-1)**i
			dt = theta/v
			w = theta/dt
			self.setSpeed(v, w, dt, motion_service)
			distance = distance + abs(theta)
			i = i+1

	def setSpeed(self, lin_vel, ang_vel, dtime, motion_service):
		motion_service.move(lin_vel,0,ang_vel)
		time.sleep(dtime)
		motion_service.stopMove()

	def circle(self, r, ms):
			#if (r>0.1):
			print 'Circle ',r
			v = 0.3
			dt = 2*math.pi*r/v
			w = 2*math.pi/dt # = v/r
			self.setSpeed(v,w,dt,ms)

	def forward(r=1):
		print 'Forward ',r
		s = 0.5*r
    		v = 0.2
    		setSpeed(v,0,abs(s/v))

	def backward(r=1):
    		print 'Backward ',r
    		s = 0.5*r
    		v = -0.2
    		setSpeed(v,0,abs(s/v))

	def left(r=1):
		print 'Left ',r
		s = (math.pi/2)*r
		w = 0.5
		setSpeed(0,w,abs(s/w))

	def right(r=1):
		print 'Right ',r
		s = (math.pi/2)*r
		w = -0.5
		setSpeed(0,w,abs(s/w))


	def playEmotion(self, emotion):
		if emotion == "happy":
			self.playHappyEmotion()
		elif emotion == "sad":
			self.playSadEmotion()
		elif emotion == "afraid":
			self.playAfraidEmotion()
                elif emotion == "angry":
                        self.playAngryEmotion()
		else:
			print "Emotion %s not recognized!" %(emotion)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
    	parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'], help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    	parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")
	parser.add_argument("--emotion", type=str, default="happy", help="Emotion to mimic. One of {'happy', 'sad', 'afraid', 'special'}")
    	#parser.add_argument("--values", type=str, default='[0.00, -0.21, 1.55, 1.13, -1.24, -0.52, 0.01, 1.56, -1.14, 1.22, 1.52, -0.01]',help="Joint values")

	args = parser.parse_args()
	pip = args.pip
	pport = args.pport
	emotion = args.emotion

	try:
        	connection_url = "tcp://" + pip + ":" + str(pport)
        	print("trying to connect to "+str(connection_url)+"\n")

        	app = qi.Application(["Eyegaze", "--qi-url=" + connection_url ])
        	print("connected to "+str(connection_url)+"\n")

	except RuntimeError:
        	print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
			"Please check your script arguments. Run with -h option for help.")
		sys.exit(1)


	motionController = PlayEmotionController(app)
	#motionController.playSadEmotion()
	#motionController.playHappyEmotion()
	motionController.playEmotion(emotion)
