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

def wave(pip, pport):
    
    TO_RAD = math.pi/180.0


    headYT = [1.0]
    headPT = [1.0]
    LShoulderPT = [1.0]
    LShoulderRT = [1.0]
    LElbowYT = [1.0]
    LElbowRT = [1.0]
    LWristYT = [1.0]
    RShoulderPT = [1.0, 2.0]
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
    LShoulderPA = [0.0]
    LShoulderRA = [0.0]
    LElbowYA = [0.0]
    LElbowRA = [0.0]
    LWristYA = [0.0]
    RShoulderPA = [45.0*TO_RAD, 0.0]
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
	#jointTimes = [[3.0], [1.0, 3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0], [3.0]]
	#jointValues = [[0.0], [20.0*TO_RAD, 0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

	# if (jointValues==None):
	#       print 'No joint values.'
	#       sys.exit(0)

    isAbsolute = True

	# Start service
    print "Executing motion..."
	#motion_service  = self.session.service("ALMotion")
    motionProxy = ALProxy("ALMotion", pip, pport)

    motionProxy.post.angleInterpolation(jointsNames, jointValues, jointTimes, isAbsolute)

    print "End motion execution"
    
 
 if __name__=='__main__':
     
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1', help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    
    wave(pip,pport)