
import mediapipe as mp 
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

def async_detect_gestures_proxy():
    
    print("Entered sub-process\n")
    
    base_dir = os.path.dirname(__file__)
    sys.path.insert(1, base_dir + 'hand-gesture-recognition-code')

    # initialize mediapipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils
    
    # Load the gesture recognizer model
    model = load_model('hand-gesture-recognition-code/mp_hand_gesture')

    # Load class names
    f = open('hand-gesture-recognition-code/gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()

    # Retrieve video
    cap = cv2.VideoCapture('videos/vtest2.avi')

    # New video writer
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter('videos/output2.avi', fourcc, fps, (width,  height))

    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...\n")
            break

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)
        
        className = ''

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]
                print(className)

        # show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,0,255), 2, cv2.LINE_AA)

        # Write the final output
        out.write(frame)

    cap.release()
    out.release()
    
    

    

if __name__ == "__main__":
    async_detect_gestures_proxy()