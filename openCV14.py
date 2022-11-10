import cv2
from cv2 import CAP_PROP_FRAME_HEIGHT
print(cv2.__version__)
def myCallback1(val):
    width=val
    height=int(width*9/16)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
def myCallback2(val):
    global xPos
    xPos=val
def myCallback3(val):
    global yPos
    yPos=val
xPos=0
yPos=0
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myTrackbars')
cv2.resizeWindow('myTrackbars',400,125)
cv2.moveWindow('myTrackbars',width,0)
cv2.createTrackbar('frameW','myTrackbars',0,1920,myCallback1)
cv2.createTrackbar('xPos','myTrackbars',0,1280,myCallback2)
cv2.createTrackbar('yPos','myTrackbars',0,720,myCallback3)
while True:
    ignore, frame=cam.read()
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',xPos,yPos)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
