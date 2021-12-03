#import qi
import argparse
import sys
import time
import os
import cv2
import numpy as np
import math

class GazeController(object):

    #def __init__(self, app, avertgaze, trackhands):
    def __init__(self, avertgaze, trackhands):
        super(GazeController, self).__init__()
        
        self.avertgaze = avertgaze

        self.trackhands = trackhands

        if (self.avertgaze == True): 
            print("Mode [B]: averted gaze\n")
        else:
            print("Mode [A]: following gaze\n")

        if(self.trackhands == True):
            print("Tracking hand gestures\n")

        '''
        app.start()
        session = app.session
        
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        
        # Get the services ALTextToSpeech
        self.tts = session.service("ALTextToSpeech")

        # Get the services ALMotion
        self.motion = session.service("ALMotion")

        # Get the services ALRobotPosture
        self.pose = session.service("ALRobotPosture")

        # Set Pepper in Stiffness On
        self.stiffnessOn()

        # Send Pepper to Pose Init
        self.pose.goToPosture("StandInit", 0.5)

        self.effectorName = "Head"

        # Active Head tracking
        isEnabled = True
        self.motion.wbEnableEffectorControl(self.effectorName, isEnabled)
        '''
        
    def run(self):
        print("Starting GazeController\n")
        try:
            # detect faces by default
            '''print("Gaze controller disabled for testing...\n")'''
            #self.async_detect_faces()

            # python 3 version
            if(self.trackhands == 1):
                self.async_detect_gestures()
            
            print("Now sleeping - press ctrlC to quit\n")
            while  True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, stopping GazeController\n")
            
            '''
            # Deactivate Head tracking
            isEnabled  = False
            self.motion.wbEnableEffectorControl(self.effectorName, isEnabled)
            #self.stiffnessOff()
            '''
            sys.exit(0)
    '''
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
        
        # HeadYaw 	Head joint twist (Z) 	        -119.5 to 119.5 	-2.0857 to 2.0857
        # HeadPitch Head joint front and back (Y) 	-40.5 to 36.5 	    -0.7068 to 0.6371

        # frame is 1920x1080

        sh_x = (value[0]+((value[2]-value[0])/2)).item()
        sh_y = (value[1]+((value[3]-value[1])/2)).item()
        
        max_frame_x = 1920
        max_frame_y = 1080

        max_angle_x = 160
        max_angle_y = 36.5

        new_angle_x = (((sh_x * max_angle_x) / max_frame_x) - 80)
        new_angle_y = (max_angle_y - ((sh_y * max_angle_y) / max_frame_y)) 
       
        names = ["HeadYaw", "HeadPitch"]
        angleList = [new_angle_x * math.pi/180.0, new_angle_y * math.pi/180.0]
        reverseAngleList = [-new_angle_x * math.pi/180.0, -new_angle_y * math.pi/180.0]

        if (self.avertgaze == True): # don't look straight

            self.motion.setAngles(names, reverseAngleList, 0.9)

        else: # look straight
            
            self.motion.setAngles(names, angleList, 0.9)
    '''
    def async_detect_gestures(self):
        print("----- Trying to call the subprocess -----\n")
        
        import pexpect
        command = "python3 vision_pepper_slave.py"
        p = pexpect.spawn(command)
        while not p.eof():
            strLine = p.readline()
            print(strLine.rstrip())
    
    '''
    def async_detect_faces(self):
        print("Initiating detection\n")
        # Define paths
        base_dir = os.path.dirname(__file__)
        prototxt_path = os.path.join('model_data/deploy.prototxt')
        caffemodel_path = os.path.join(base_dir + 'model_data/weights.caffemodel')

        # Read the model
        model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
        
        # Retrieve video
        cap = cv2.VideoCapture('videos/vtest.avi')

        # New video writer
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter('videos/output.avi', fourcc, fps, (width,  height))

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
    '''

if __name__ == "__main__":
    cv2_version = cv2.__version__
    print("Using opencv version "+ str(cv2_version) +"\n")
    
    parser = argparse.ArgumentParser()
    '''
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'], 
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    '''
    parser.add_argument("--pip", type=str, default='127.0.0.1', 
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number.")
    parser.add_argument("--avertgaze", type=bool, default=True,
                        help="Robot behaviour: following/averting gaze.")
    parser.add_argument("--trackhands", type=int, default=1,
                        help="Robot behaviour: recognize gestures [0] no hand tracking enabled, [1] python3 version")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    avertgaze = args.avertgaze
    trackhands = args.trackhands

    '''
    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        print("trying to connect to "+str(connection_url)+"\n")
        app = qi.Application(["Eyegaze", "--qi-url=" + connection_url ])
        print("connected to "+str(connection_url)+"\n")
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    GazeController = GazeController(app, avertgaze, trackhands)

    '''
    GazeController = GazeController(avertgaze, trackhands)

    GazeController.run()
