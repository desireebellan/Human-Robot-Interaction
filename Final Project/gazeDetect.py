#!usr/bin/env python
# coding=utf-8

import qi
import argparse
import sys
import time
import os
import cv2
import numpy as np
import math
import subprocess
import struct
import pickle

from naoqi import ALProxy
from threading import Thread

class GazeController(object):

    def __init__(self, avertgaze,pip = '127.0.0.1', pport = 9559):
        super(GazeController, self).__init__()
        
        self.avertgaze = avertgaze
	self.stop_thread = False

        if self.avertgaze: 
            print("Mode [B]: averted gaze\n")
        else:
            print("Mode [A]: following gaze\n")
	
        # Get the services ALMotion
        self.motion = ALProxy("ALMotion", pip, pport )
        # Set Pepper in Stiffness On
        self.stiffnessOn()
        self.effectorName = "Head"
        # Active Head tracking
        isEnabled = True
        self.motion.wbEnableEffectorControl(self.effectorName, isEnabled)
        
    def run(self):
            print("Starting GazeController\n")
            # detect faces by default
            self.async_detect_faces()
            
            print("Now sleeping - press ctrlC to quit\n")
            while  True:
               time.sleep(1)
               if self.stop_thread:
			print " Closing the camera..."
			self.stop()

    def stiffnessOn(self):
        pNames = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def stiffnessOff(self):
        pNames = "Body"
        pStiffnessLists = 0.0
        pTimeLists = 0.0
        self.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def stop(self):
        print("Interrupted by user, stopping GazeController\n")
            
        # Deactivate Head tracking
        isEnabled  = False
        self.motion.wbEnableEffectorControl(self.effectorName, isEnabled)
        self.stiffnessOff()
	self.cap.release()
	self.out.release()
	cv2.destroyAllWindows()
        sys.exit(0)

        
    def on_human_tracked(self, key, value, message):
        
        # HeadYaw 	Head joint twist (Z) 	        -119.5 to 119.5 	-2.0857 to 2.0857
        # HeadPitch Head joint front and back (Y) 	-40.5 to 36.5 	    -0.7068 to 0.6371
        # frame is 1920x1080
        sh_x = (value[0]+((value[2]-value[0])/2)).item()
        sh_y = (value[1]+((value[3]-value[1])/2)).item()

	# Qui ho modificato i valori i risoluzione
       
        max_frame_x = 1024
        max_frame_y = 768
        max_angle_x = 160
        max_angle_y = 36.5
        new_angle_x = (((sh_x * max_angle_x) / max_frame_x) - 80)
        new_angle_y = (max_angle_y - ((sh_y * max_angle_y) / max_frame_y)) 
       
        names = ["HeadYaw", "HeadPitch"]
        angleList = [new_angle_x * math.pi/180.0, new_angle_y * math.pi/180.0]
        reverseAngleList = [-new_angle_x * math.pi/180.0, -new_angle_y * math.pi/180.0]

	# Da qui in poi il codice non va avanti

        if (self.avertgaze == True): # don't look straight
            self.motion.setAngles(names, reverseAngleList, 0.9)
        else: # look straight
            self.motion.setAngles(names, angleList, 0.9)

    def async_detect_faces(self):
        print("Initiating detection\n")
        # Define paths
        #base_dir = os.path.dirname(__file__) +'/'

        prototxt_path = os.path.join('./model_data/deploy.prototxt')
        caffemodel_path = os.path.join('./model_data/weights.caffemodel')
        # Read the model
        model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
        
        # Retrieve video
	self.cap = cv2.VideoCapture("/dev/video0")
        # New video writer
        fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        fps = float(self.cap.get(cv2.CAP_PROP_FPS))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.out = cv2.VideoWriter('videos/output_0.avi', fourcc, fps, (width,  height))
        while self.cap.isOpened() and not self.stop_thread:
            ret, frame = self.cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...\n")
                break
            
            # Face detection
            image = frame
            
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            model.setInput(blob)
            detections = model.forward()
            # Create frame around face
            for i in range(0, detections.shape[2]):
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                confidence = detections[0, 0, i, 2]
                # If confidence > 0.5, show box around face
                if (confidence > 0.5):
                    cv2.rectangle(image, (startX, startY), (endX, endY), (255, 255, 255), 2)
                    cv2.circle(image, (startX + abs(endX-startX)/2, startY + abs(endY-startY)/2), radius=10, color=(0, 0, 255), thickness=-1)
                    # call 
                    self.on_human_tracked("key", box.astype("int"), "message")
                
            # Write the new frame
	    cv2.imshow("Image", image)
            cv2.waitKey(1)
            self.out.write(image)
        self.cap.release()
        self.out.release()
	cv2.destroyAllWindows()
        print("Detection completed\n")

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--avertgaze", type = bool, default = True)
    	parser.add_argument("--pip", type=str, default='127.0.0.1', help="Robot IP address.  On robot or Local Naoget: use '127.0.0.1'.")
    	parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")

	args = parser.parse_args()
	avertgaze = args.avertgaze
    	pip = args.pip
    	pport = args.pport

	gaze = GazeController(avertgaze, pip, pport)
	gaze.run()
