import cv2
import numpy as np

print(cv2.__version__)
width=640
height=360
evt=0
def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global xVal
    global yVal
    if event==cv2.EVENT_LBUTTONDOWN:
        evt=event
        xVal=xPos
        yVal=yPos

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myWEBCAM')
cv2.setMouseCallback('myWEBCAM',mouseClick)
while True:
    ignore, frame=cam.read()
    if evt==1:
        x=np.zeros([200,200,3],dtype=np.uint8)
        y=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        clr=y[yVal][xVal]
        print(clr)
        x[:,:]=clr
        cv2.imshow('colorWindow',x)
        cv2.moveWindow('colorWindow',width,0)
        evt=0
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
