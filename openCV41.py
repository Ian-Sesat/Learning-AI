import cv2
import numpy as np
print(cv2.__version__)

class mpHands:
    def __init__(self,numHands=2,tol1=.5,tol2=.5):
        import mediapipe as mp
        self.hands=mp.solutions.hands.Hands(False,numHands,tol1,tol2)
    def myHands(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        myHands=[]
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width), int(landMark.y*height)))
                myHands.append(myHand)
        return myHands

def findDistances(handData):
    distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):
            distMatrix[row][column]=((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.)
    return distMatrix
def findError(gestureMatrix,unKnownMatrix,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unKnownMatrix[row][column])
    return error
            

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
keyPoints=[0,1,5,9,13,17,4,8,12,16,20]
findHands=mpHands(1)
training=True

while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    myHands=findHands.myHands(frame)
    if training == True:
        if myHands!=[]:
            print('Show your gesture, press t when ready')
            if cv2.waitKey(1)& 0xff== ord('t'):
                knownGesture=findDistances(myHands[0])
                #print(knownGesture)
                training=False
    if training==False:
        if myHands!=[]:
            unKnownGesture=findDistances(myHands[0])
            error=findError(knownGesture,unKnownGesture,keyPoints)
            cv2.putText(frame,str(int(error)),(100,100),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),5)

    for hand in myHands:
        for ind in keyPoints:
            cv2.circle(frame,hand[ind],20,(255,0,255),3)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()

