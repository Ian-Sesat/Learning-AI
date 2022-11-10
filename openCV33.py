import cv2
print(cv2.__version__)
class mpHands():
    def __init__(self,numHands=2,tol1=.5,tol2=.5):
        import mediapipe as mp
        self.hands=mp.solutions.hands.Hands(False,numHands,tol1,tol2)
    def myHandsArray(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        myHands=[]
        handTypes=[]
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            print(results.multi_handedness)
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                #print(hand.classification[0].label)
                handTypes.append(hand.classification[0].label)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handTypes

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(2)
while True:
    ignore, frame=cam.read()
    myHands,handTypes=findHands.myHandsArray(frame)
    for hand,handType in zip(myHands,handTypes):
        if handType=='Right':
            handColor=(255,0,0)
        else:
            handColor=(0,0,255)
        for ind in [13,14,15,16]:
            cv2.circle(frame,hand[ind],20,handColor,3)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
