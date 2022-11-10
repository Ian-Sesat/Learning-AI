import cv2
import numpy as np
print(cv2.__version__)

width=640
height=360
def onCall1(val):
    global hueLow
    hueLow=val
def onCall2(val):
    global hueHigh
    hueHigh=val
def onCall3(val):
    global satLow
    satLow=val
def onCall4(val):
    global satHigh
    satHigh=val
def onCall5(val):
    global valLow
    valLow=val
def onCall6(val):
    global valHigh
    valHigh=val

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myTrackbars')
cv2.resizeWindow('myTrackbars',320,300)
cv2.moveWindow('myTrackbars',width,0)
cv2.createTrackbar('hueLow','myTrackbars',10,179,onCall1)
cv2.createTrackbar('hueHigh','myTrackbars',20,179,onCall2)
cv2.createTrackbar('satLow','myTrackbars',10,255,onCall3)
cv2.createTrackbar('satHigh','myTrackbars',250,255,onCall4)
cv2.createTrackbar('valLow','myTrackbars',10,255,onCall5)
cv2.createTrackbar('valHigh','myTrackbars',250,255,onCall6)

while True:
    ignore, frame=cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    myObject=cv2.bitwise_and(frame,frame,mask=myMask)
    myObject=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('myObject',myObject)
    cv2.moveWindow('myObject',int(width/2),height)
    cv2.imshow('myMaskSmall',myMaskSmall)
    cv2.moveWindow('myMaskSmall',0,height)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
