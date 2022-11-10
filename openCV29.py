from cv2 import VideoCapture
import mediapipe as mp
import cv2
print(cv2.__version__)

width=1280
height=720
hands=mp.solutions.hands.Hands(False,2,.5,.5)

def parseLandmarks(frame):
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB)
    myHands=[]
    if results.multi_hand_landmarks != None:
        for handLandMarks in results.multi_hand_landmarks:
            myHand=[]
            for landmark in handLandMarks.landmark:
                myHand.append((int(landmark.x*width), int(landmark.y*height)))
            #print(myHand)
            myHands.append(myHand)
    return myHands

cam=VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

while True:
    ignore, frame=cam.read()
    myHands=parseLandmarks(frame)
    for myHand in myHands:
        for dig in [8,12,16,20]:
            cv2.circle(frame,myHand[dig],(20),(255,0,255),3)

    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()