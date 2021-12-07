import qi
import argparse
import sys
import time
import os
import cv2
import numpy as np
import math

from naoqi import ALProxy

class GazeController(object):

    def __init__(self, avertgaze,pip = '127.0.0.1', pport = 9559):
        super(GazeController, self).__init__()
        
        self.avertgaze = avertgaze

        if self.avertgaze: 
            print("Mode [B]: averted gaze\n")
        else:
            print("Mode [A]: following gaze\n")

	# questa parte, essendo passta completamente a naoqi, non serve in realtà a nulla	
	
	'''
        self.session = qi.Session()
	self.session.connect("tcp://127.0.0.1:9559")
	'''

	# non ho capito bene a cosa servissero ALMemory, ALSpeech e ALRobotPosture. Misembra non avessero utilità nel codice e li ho tolti. Il codice da solo comunque funziona lo stesso
        
        # Get the service ALMemory.
	#memory = self.session.service("ALMemory")
	#subscriber = memory.subscriber("FaceDetected")
	#subscriber.signal.connect(self.on_human_tracked) 
	
        print "motion"
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
        try:
            # detect faces by default
            self.async_detect_faces()
            
            print("Now sleeping - press ctrlC to quit\n")
            while  True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, stopping GazeController\n")
            
            # Deactivate Head tracking
            isEnabled  = False
            self.motion.wbEnableEffectorControl(self.effectorName, isEnabled)
            self.stiffnessOff()
            sys.exit(0)

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
    def on_human_tracked(self, key, value, message):
	print "checkpoint 5"
        
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
	print "checkpoint 6"

	# Da qui in poi il codice non va avanti

        if (self.avertgaze == True): # don't look straight
            self.motion.setAngles(names, reverseAngleList, 0.9)
        else: # look straight
            
            self.motion.setAngles(names, angleList, 0.9)
	print " checkpoint 7"

    def async_detect_faces(self):
        print("Initiating detection\n")
        # Define paths
        base_dir = os.path.dirname(__file__) +'/'
        prototxt_path = os.path.join('model_data/deploy.prototxt')
        caffemodel_path = os.path.join(base_dir + 'model_data/weights.caffemodel')
        # Read the model
        model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
	print "checkpoint 2"
        
        # Retrieve video
	# Qui l'ho provato sia con uno dei video caricati di Edoardo sia con la mia webcam
        cap = cv2.VideoCapture('videos/vtest.avi')
	#cap = cv2.VideoCapture("/dev/video0")
	print "checkpoint 3"
        # New video writer
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter('videos/output_0.avi', fourcc, fps, (width,  height))
	print cap.isOpened()
	print"checkpoint 4"
        while cap.isOpened():
            ret, frame = cap.read()
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
            out.write(image)
        cap.release()
        out.release()
        print("Detection completed\n")



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--pip", type=str, default='127.0.0.1', 
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number.")
    parser.add_argument("avertgaze", type=bool, default=True,
                        help="Robot behaviour: following/averting gaze.")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    avertgaze = args.avertgaze

    #Starting application
    '''
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        print("trying to connect to "+str(connection_url)+"\n")
        app = qi.Application(["Eyegaze", "--qi-url=" + connection_url ])
        print("connected to "+str(connection_url)+"\n")
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    '''
    gazeController = GazeController(app, avertgaze, pip, pport )

    gazeController.run()

