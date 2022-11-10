import cv2
import mediapipe as mp

print(cv2.__version__)
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

#creating mediapipe objects forhands and drawing utilities for mediapipe
hands=mp.solutions.hands.Hands(False,2,.5,.5)
mpDraw=mp.solutions.drawing_utils
while True:
    ignore, frame=cam.read()
    myHands=[]
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB)
    if results.multi_hand_landmarks!= None:
        for handLandmarks in results.multi_hand_landmarks:
            myHand=[]
            #mpDraw.draw_landmarks(frame,handLandmarks,mp.solutions.hands.HAND_CONNECTIONS)
            for landmark in handLandmarks.landmark:
                #print((int(landmark.x*width),int(landmark.y*height)))
                xPos=int(landmark.x*width)
                yPos=int(landmark.y*height)
                landmarkPoints=(xPos,yPos)
                myHand.append(landmarkPoints)
            #print(myHand)
            #print('')
            cv2.circle(frame,myHand[20],15,(0,0,255),-1)
            cv2.circle(frame,myHand[18],15,(0,0,255),-1)
            cv2.circle(frame,myHand[19],15,(0,0,255),-1)
            cv2.circle(frame,myHand[17],15,(0,0,255),-1)
            myHands.append(myHand)
        print(myHands)
        print('')

    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
