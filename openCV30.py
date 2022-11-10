import cv2
from cv2 import COLOR_BGR2RGB
print(cv2.__version__)

#Creating a class for parsing the landmark data :
class mpHands:
    def __init__(self,numHands=2,tol1=.5,tol2=.5):
        import mediapipe as mp
        self.hands=mp.solutions.hands.Hands(False,numHands,tol1,tol2)
    def myHands(self,frame):
        frameRGB=cv2.cvtColor(frame,COLOR_BGR2RGB)
        myHands=[]
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width), int(landMark.y*height)))
                myHands.append(myHand)
            print(myHands)
            print('')
        return myHands

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

#calling the clas made above to make the hands object :
findHands=mpHands(2)

while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    myHands=findHands.myHands(frame)
    for hand in myHands:
        for ind in [13,14,15,16]:
            cv2.circle(frame,hand[ind],20,(255,0,255),3)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()

