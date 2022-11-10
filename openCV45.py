import cv2
print(cv2.__version__)
import numpy as np
import pickle
import serial

arduinoData=serial.Serial('COM7',115200)
height=720
width=1280

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
    palmSize=((handData[0][0]-handData[9][0])**2+(handData[0][1]-handData[9][1])**2)**(1./2.)
    for row in range(0,len(handData),1):
        for column in range(0,len(handData),1):
            distMatrix[row][column]=(((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.))/palmSize
    return distMatrix

def error(gestureMatrix,unknownGesture,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unknownGesture[row][column])
    return error

def findGestures(knownGestures,unknownGesture,keyPoints,gestNames,tol):
    errorArray=[]
    for i in range(0,len(gestNames),1):
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

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
keyPoints=[0,1,5,9,13,17,4,8,12,16,20]
tol=20
train=int(input('Are you training or recognizing, Press 0 to recognize and 1 if it is to train '))

if train==1:
    knownGestures=[]
    trainCnt=0
    gestNames=[]
    numGest=int(input('How many gestures do you want to train on ? '))
    for i in range(0,numGest,1):
        prompt='Please specify the gesture you want to train on #'+str(i+1)+' '
        gestName=input(prompt)
        gestNames.append(gestName)
    trainName=input('FileName to store trained data: , if default press Enter ')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'

if train==0:
    trainName=input('From which file do you want to recognize the gestures? if default press Enter ')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'
    with open(trainName,'rb') as f:
        gestNames=pickle.load(f)
        knownGestures=pickle.load(f)

findHands=mpHands(1)

while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    myHands=findHands.marks(frame)
    for hand in myHands:
        for i in keyPoints:
            cv2.circle(frame,hand[i],20,(255,0,255),3)
    if train==1:
        if myHands!=[]:
            print('Please train on the gesture: '+gestNames[trainCnt],' press t when ready')
            if cv2.waitKey(1)&0xff == ord('t'):
                knownGesture=findDistances(myHands[0])
                knownGestures.append(knownGesture)
                trainCnt=trainCnt+1
                if trainCnt==numGest:
                    train=0
                    with open (trainName,'wb') as f:
                        pickle.dump(gestNames,f)
                        pickle.dump(knownGestures,f)
    if train==0:
        if myHands!=[]:
            unknownGesture=findDistances(myHands[0])
            gesture=findGestures(knownGestures,unknownGesture,keyPoints,gestNames,tol)

            cv2.putText(frame,gesture,(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),3)
            gesture=gesture+'\r'
            arduinoData.write(gesture.encode())


    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()