
import hand_tracking_module as htm
import cv2
import time

def async_detect_gestures_proxy():
    
    print("Entered sub-process\n")
    
    # Retrieve video
    cap = cv2.VideoCapture(0)

    # New video writer
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter('videos/output2.avi', fourcc, fps, (width,  height))

    pTime=0

    detector=htm.handDetector(detectionCon=0.75)
    tipIds=[4,8,12,16,20]

    while cap.isOpened():
        ret, img = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...\n")
            break
        
        img=detector.findHands(img)
        lmList=detector.findPosition(img,draw=False)
        #print(lmList)
        if len(lmList) !=0:
            fingers=[]

            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1,5):  #y axis
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers=fingers.count(1)
            print(totalFingers)

            cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
            cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)
        
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        
        cv2.putText(img,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.imshow("Image",img)
        out.write(img)
        cv2.waitKey(1)

    cap.release()
    out.release()
    
if __name__ == "__main__":
    async_detect_gestures_proxy()
