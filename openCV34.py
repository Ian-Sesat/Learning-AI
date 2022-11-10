import cv2
print(cv2.__version__)
class mpHands:
    def __init__(self,numHands=2,tol1=.5,tol2=.5):
        import mediapipe as mp
        self.hands=mp.solutions.hands.Hands(False,numHands,tol1,tol2)
    def myHandsArray(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        myHands=[]
        myHandTypes=[]
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                myHandTypes.append(hand.classification[0].label)
            for handLandmarks in results.multi_hand_landmarks:
                myHand=[]
                for landmark in handLandmarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myHands.append(myHand)
        return myHands,myHandTypes

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

ballRadius=25
ballColor=(0,255,0)
xPos=int(width/2)
yPos=int(height/2)
deltaX=4
deltaY=4
paddleWidth=40
paddleHeight=125
paddleColor=(0,0,255)
font=cv2.FONT_HERSHEY_SIMPLEX
fontScale=3
fontColor=(0,0,255)
fontThickness=3
scoreLeft=0
scoreRight=0
yleftTip=0
yrightTip=0

findHands=mpHands(2)
while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    cv2.putText(frame,str(scoreLeft),(75,125),font,fontScale,fontColor,fontThickness)
    cv2.putText(frame,str(scoreRight),(width-100,125),font,fontScale,fontColor,fontThickness)
    cv2.circle(frame,(xPos,yPos),ballRadius,ballColor,-1)
    myHands,myHandsTypes=findHands.myHandsArray(frame)
    for myHand,myHandType in zip(myHands,myHandsTypes):
        if myHandType=='Right':
            yrightTip=myHand[8][1]
        if myHandType=='Left':
            yleftTip=myHand[8][1]
    cv2.rectangle(frame,(0,int(yleftTip-paddleHeight/2)),(paddleWidth,int(yleftTip+paddleHeight/2)),paddleColor,-1)
    cv2.rectangle(frame,(width-paddleWidth,int(yrightTip-paddleHeight/2)),(width,int(yrightTip+paddleHeight/2)),paddleColor,-1)
    topBallEdge=yPos-ballRadius
    bottomBallEdge=yPos+ballRadius
    leftBallEdge=xPos-ballRadius
    rightBallEdge=xPos+ballRadius
    if topBallEdge <=0 or bottomBallEdge>= height:
        deltaY=deltaY*(-1)
    if leftBallEdge <= paddleWidth:
        if yPos<=int(yleftTip+paddleHeight/2) and yPos>=int(yleftTip-paddleHeight/2):
            deltaX=deltaX*(-1)
        else:
            xPos=int(width/2)
            yPos=int(height/2)
            scoreRight=scoreRight+1
    if rightBallEdge >= width-paddleWidth:
        if yPos<=int(yrightTip+paddleHeight/2) and yPos>=int(yrightTip-paddleHeight/2):
            deltaX=deltaX*(-1)
        else:
            xPos=int(width/2)
            yPos=int(height/2)
            scoreLeft=scoreLeft+1
    xPos=xPos+deltaX
    yPos=yPos+deltaY
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if scoreLeft-scoreRight==5:
        break
    if scoreRight-scoreLeft==5:
        break
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
