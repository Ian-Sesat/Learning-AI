import cv2
print(cv2.__version__)
width=1280
height=720
def myCallBack1(val):
    global xPos
    print(val)
    xPos=val
def myCallBack2(val):
    global yPos
    print(val)
    yPos=val
def myCallBack3(val):
    global myRad
    print(val)
    myRad=val
def myCallBack4(val):
    global myThick
    print(val)
    myThick=val

xPos=int(width/2)
yPos=int(height/2)
myRad=25
myThick=1
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myTrackbars')
cv2.resizeWindow('myTrackbars',400,150)
cv2.moveWindow('myTrackbars',width,0)
cv2.createTrackbar('xPos','myTrackbars',xPos,width,myCallBack1)
cv2.createTrackbar('yPos','myTrackbars',yPos,height,myCallBack2)
cv2.createTrackbar('radius','myTrackbars',myRad,int(height/2),myCallBack3)
cv2.createTrackbar('myThick','myTrackbars',myThick,10,myCallBack4)

while True:
    ignore, frame=cam.read() 
    if myThick==10:
        myThick=-1
    cv2.circle(frame,(xPos,yPos),myRad,(255,0,0),myThick)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
