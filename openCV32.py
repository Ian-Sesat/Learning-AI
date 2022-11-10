#The classic Pong arcade game program
import cv2
print(cv2.__version__)

class mpHands():
    def __init__(self,numHands=2,tol1=.5,tol2=.5):
        import mediapipe as mp
        self.hands=mp.solutions.hands.Hands(False,numHands,tol1,tol2)
    def numHandsArray(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        myHands=[]
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landmark in handLandMarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myHands.append(myHand)
        return myHands

height=720
width=1280               
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
paddleWidth=125
paddleHeight=25
paddleColor=(0,0,255)
font=cv2.FONT_HERSHEY_SIMPLEX
lives=3
score=0
ballRadius=25
ballColor=(0,255,0)
ballThickness=-1
xPos=int(width/2)
yPos=int(height/2)
deltaX=4
deltaY=4

findHands=mpHands(1)
while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    cv2.circle(frame,(xPos,yPos),ballRadius,ballColor,ballThickness)
    cv2.putText(frame,'Score:',(10,int(2*paddleHeight)),font,1,(0,0,255),2)    
    cv2.putText(frame,str(score),(25,int(6*paddleHeight)),font,4,(0,0,255),3)
    cv2.putText(frame,'Lives:',(width-100,int(2*paddleHeight)),font,1,(0,0,255),2)  
    cv2.putText(frame,str(lives),(width-100,int(6*paddleHeight)),font,4,(0,0,255),3)
    myHandsData=findHands.numHandsArray(frame)
    for hand in myHandsData:
        cv2.rectangle(frame,(int(hand[8][0]-paddleWidth/2),0),(int(hand[8][0]+paddleWidth/2),paddleHeight),paddleColor,-1)
    topEdgeBall=yPos-ballRadius
    bottomEdgeBall=yPos+ballRadius
    leftEdgeBall=xPos-ballRadius
    rightEdgeBall=xPos+ballRadius
    if leftEdgeBall <=0 or rightEdgeBall>=width:
        deltaX=deltaX*(-1)
    if bottomEdgeBall>=height:
        deltaY=deltaY*(-1)
    if topEdgeBall <= paddleHeight:
        if xPos >= int(hand[8][0]- paddleWidth/2) and xPos <= int(hand[8][0]+paddleWidth/2):
            deltaY=deltaY*(-1)
            score=score+1
            if score==5 or score==10 or score==15 or score==20:
                deltaX=deltaX*2
                deltaY=deltaY*2
        else:
            xPos=int(width/2)
            yPos=int(height/2)
            lives=lives-1
 
    xPos=xPos+deltaX
    yPos=yPos+deltaY
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',200,100)

    if lives==0:
        break
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()