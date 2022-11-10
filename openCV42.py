import cv2
print(cv2.__version__)
import numpy as np
import time

class mpHands:
    import mediapipe as mp
    def __init__(self,numHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(False,numHands,tol1,tol2)
    def marks(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        myHands=[]
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks!=None:
            for handLandmarks in results.multi_hand_landmarks:
                myHand=[]
                for landmark in handLandmarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myHands.append(myHand)
        return myHands

def findDistances(handData):
    distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
    for row in range(0,len(handData),1):
        for column in range(0,len(handData)):
            distMatrix[row][column]=((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.)
    return distMatrix

def error(gestureMatrix,unknownMatrix,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unknownMatrix[row][column])
    return error

def findGesture(knownGestures,unknownGesture,keyPoints,gestNames,tol):
    errorArray=[]
    for i in range(0,len(gestNames)):
        err=error(knownGestures[i],unknownGesture,keyPoints)
        errorArray.append(err)
    errorMin=errorArray[0]
    minIndex=0
    for i in range(0,len(errorArray),1):
        if errorArray[i]<errorMin:
            errorMin=errorArray[i]
            minIndex=i
    if errorMin<tol:
        gesture=gestNames[minIndex]
    if errorMin>=tol:
        gesture='unKnown'
    return gesture

time.sleep(2)
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

keyPoints=[0,1,5,9,13,17,4,8,12,16,20]
tol=1500

numGestures=int(input('How many gestures do you want? '))
gestNames=[]
for i in range(0,numGestures,1):
    prompt='Please, enter your gesture name'+str(i+1)+' '
    name=input(prompt)
    gestNames.append(name)
train=True
trainCount=0
knownGestures=[]
findHands=mpHands(1)

while True:
    ignore, frame=cam.read()
    myHands=findHands.marks(frame)
    if train == True:
        if myHands!=[]:
            print('Please, show your gesture, the gesture being '+gestNames[trainCount]+' press t when ready ')
            if cv2.waitKey(1)& 0xff == ord('t'):
                knownGesture=findDistances(myHands[0])
                knownGestures.append(knownGesture)
                trainCount=trainCount+1
                if trainCount==numGestures:
                    train=False
    if train== False:
        if myHands!=[]:
            unKnownGesture=findDistances(myHands[0])
            gesture=findGesture(knownGestures,unKnownGesture,keyPoints,gestNames,tol)
            cv2.putText(frame,gesture,(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)
    for hand in myHands:
        for i in keyPoints:
            cv2.circle(frame,hand[i],15,(255,0,255),2)      
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)& 0xff==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

