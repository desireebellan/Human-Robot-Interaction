import qi
import argparse
import sys
import time
import os
import math

from naoqi import ALProxy


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
	def __init__(self,pip,pport):
		super(PlayEmotionController, self).__init__()
		self.pip = pip
		self.pport = pport
	#--------------#
	#-----RESET----#
	#--------------#

	def reset(self, joint_values = None):

    		TO_RAD = math.pi/180.0


		headYT = [1.0]
		headPT = [1.0]
		LShoulderPT = [1.0]
		LShoulderRT = [1.0]
		LElbowYT = [1.0]
		LElbowRT = [1.0]
		LWristYT = [1.0]
		RShoulderPT = [1.0]
		RShoulderRT = [1.0]
		RElbowYT = [1.0]
		RElbowRT = [1.0]
		RWristYT = [1.0]
		HipRT = [1.0]
                HipPT = [1.0]
                RHandT = [1.0]
                LHandT = [1.0]

		headYA = [0.0]
		headPA = [0.0]
		LShoulderPA = [90*TO_RAD]
		LShoulderRA = [0.0]
		LElbowYA = [0.0]
		LElbowRA = [0.0]
		LWristYA = [0.0]
		RShoulderPA = [90*TO_RAD]
		RShoulderRA = [0.0]
		RElbowYA = [0.0]
		RElbowRA = [0.0]
		RWristYA = [0.0]
		HipRA = [0.0]
                HipPA = [0.0]
                RHandA = [0.0]
                LHandA = [0.0]

		jointTimes = [headYT, headPT, LShoulderPT, LShoulderRT, LElbowYT, LElbowRT,
                              LWristYT, RShoulderPT, RShoulderRT, RElbowYT, RElbowRT, RWristYT, HipRT, HipPT, RHandT, LHandT]

		jointValues = [headYA, headPA, LShoulderPA, LShoulderRA, LElbowYA, LElbowRA,
                               LWristYA, RShoulderPA, RShoulderRA, RElbowYA, RElbowRA, RWristYA, HipRA, HipPA, RHandA, LHandA]

		isAbsolute = True

		# Start service
		print "Executing motion..."
		motionProxy = ALProxy("ALMotion", self.pip, self.pport)

                motionProxy.post.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)

		print "End motion execution"



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

		isAbsolute = True

		# Start service
		print "Executing motion..."
		motionProxy = ALProxy("ALMotion", self.pip, self.pport)

                motionProxy.post.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)

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

                isAbsolute = True

                # Start service
                print "Executing motion..."
		motionProxy = ALProxy("ALMotion", self.pip, self.pport)

                motionProxy.post.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)

                print "End motion execution"


	# ================== #
	# Surprised Gestures #
	# ================== #
	def playSurprisedEmotion(self, joint_values = None):

                TO_RAD = math.pi/180.0


                headYT = [3.0]
                headPT = [3.0]
                LShoulderPT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
                LShoulderRT = [1.0, 2.0, 3.0, 4.0, 5.0]
                LElbowYT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
                LElbowRT = [1.0, 3.0, 4.0, 5.0, 6.0]
                LWristYT = [1.0, 2.0, 3.0, 4.0]
                RShoulderPT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
                RShoulderRT = [1.0, 2.0, 3.0, 4.0, 5.0]
                RElbowYT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
                RElbowRT = [1.0, 3.0, 4.0, 5.0, 6.0]
                RWristYT = [1.0, 2.0, 3.0, 4.0]
                HipRT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
                HipPT = [1.0, 2.0, 3.0]
                RHandT = [2.0]
                LHandT = [2.0]


                headYA = [0.0]
                headPA = [0.0]
                LShoulderPA = [50.0*TO_RAD, -20.0*TO_RAD, 20.0*TO_RAD, 20.0*TO_RAD, 70.0*TO_RAD, -45.0*TO_RAD]
                LShoulderRA = [0.0, 26.0*TO_RAD, 0.0, 0.0, 26.0*TO_RAD]
                LElbowYA = [-70.0*TO_RAD, -70.0*TO_RAD, -60.0*TO_RAD, -45.0*TO_RAD, -100.0*TO_RAD, -30.0*TO_RAD]
                LElbowRA = [-85.0*TO_RAD, -90.0*TO_RAD, -90.0*TO_RAD, -50.0*TO_RAD, -98.0*TO_RAD]
                LWristYA = [0.0, -20.0*TO_RAD, -20.0*TO_RAD, -80.0*TO_RAD]
                RShoulderPA = [50.0*TO_RAD, -20.0*TO_RAD, 20.0*TO_RAD, 20.0*TO_RAD, 70.0*TO_RAD, -45.0*TO_RAD]
                RShoulderRA = [0.0, -26.0*TO_RAD, 0.0, 0.0, -26.0*TO_RAD]
                RElbowYA = [70.0*TO_RAD, 70.0*TO_RAD, 60.0*TO_RAD, 45.0*TO_RAD, 100.0*TO_RAD, 30.0*TO_RAD]
                RElbowRA = [85.0*TO_RAD, 90.0*TO_RAD, 90.0*TO_RAD, 50.0*TO_RAD, 98.0*TO_RAD]
                RWristYA = [0.0, 20.0*TO_RAD, 20.0*TO_RAD, 80.0*TO_RAD]
                HipRA = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -15.0*TO_RAD, 0.0, 15.0*TO_RAD, 0.0]
                HipPA = [0.0, 5.0*TO_RAD, 0.0]
                RHandA = [96.0*TO_RAD]
                LHandA = [96.0*TO_RAD]

                jointTimes = [headYT, headPT, LShoulderPT, LShoulderRT, LElbowYT, LElbowRT,
                              LWristYT, RShoulderPT, RShoulderRT, RElbowYT, RElbowRT, RWristYT, HipRT, HipPT, RHandT, LHandT]

                jointValues = [headYA, headPA, LShoulderPA, LShoulderRA, LElbowYA, LElbowRA,
                               LWristYA, RShoulderPA, RShoulderRA, RElbowYA, RElbowRA, RWristYA, HipRA, HipPA, RHandA, LHandA]

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

                isAbsolute = True

                # Start service
                print "Executing motion..."
		motionProxy = ALProxy("ALMotion", self.pip, self.pport)

                motionProxy.post.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)


                print "End motion execution"


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


