import cv2
print(cv2.__version__)
class mpHands:
    def __init__(self,nuMhands=2,tol1=0.5,tol2=.5):
        import mediapipe as mp
        self.hands=mp.solutions.hands.Hands(False,nuMhands,tol1,tol2)
    def myHandsArray (self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        myHands=[]
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handlandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landmark in handlandMarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myHands.append(myHand)

        return myHands

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
paddleWidth=125
paddleHeight=25
paddleColor=(0,255,0)

findHands=mpHands(1)

while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    myHandsData=findHands.myHandsArray(frame)
    for hand in myHandsData:
        cv2.rectangle(frame,(int(hand[8][0]-paddleWidth/2),0),(int(hand[8][0]+paddleWidth/2),paddleHeight),paddleColor,-1)

    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()