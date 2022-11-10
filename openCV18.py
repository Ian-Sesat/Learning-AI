import cv2
import numpy as np

print(cv2.__version__)
hueLow1=15
hueHigh1=30
hueLow2=50
hueHigh2=60
satLow=10
satHigh=255
vLow=10
vHigh=255

width=640
height=360
def oncall1(val):
    global hueLow1
    hueLow1=val
def oncall2(val):
    global hueHigh1
    hueHigh1=val
def oncall3(val):
    global hueLow2
    hueLow2=val
def oncall4(val):
    global hueHigh2
    hueHigh2=val
def oncall5(val):
    global satLow
    satLow=val 
def oncall6(val):
    global satHigh
    satHigh=val
def oncall7(val):
    global vLow
    vLow=val
def oncall8(val):
    global vHigh
    vHigh=val

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myTrackbars')
cv2.resizeWindow('myTrackbars',400,360)
cv2.moveWindow('myTrackbars',width,0)
cv2.createTrackbar('hueLow1','myTrackbars',10,179,oncall1)
cv2.createTrackbar('hueHigh1','myTrackbars',20,179,oncall2)
cv2.createTrackbar('hueLow2','myTrackbars',10,179,oncall3)
cv2.createTrackbar('hueHigh2','myTrackbars',20,179,oncall4)
cv2.createTrackbar('satLow','myTrackbars',10,255,oncall5)
cv2.createTrackbar('satHigh','myTrackbars',250,255,oncall6)
cv2.createTrackbar('valLow','myTrackbars',20,255,oncall7)
cv2.createTrackbar('valHigh','myTrackbars',250,255,oncall8)

while True:
    ignore, frame=cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow1,satLow,vLow])
    upperBound=np.array([hueHigh1,satHigh,vHigh])
    lowerBound2=np.array([hueLow2,satLow,vLow])
    upperBound2=np.array([hueHigh2,satHigh,vHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    myMask2=cv2.inRange(frameHSV,lowerBound2,upperBound2)
    myMaskComposite=myMask | myMask2
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    myMaskSmall2=cv2.resize(myMask2,(int(width/2),int(height/2)))
    myObject=cv2.bitwise_and(frame,frame,mask=myMaskComposite)
    myObject=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('myObject',myObject)
    cv2.moveWindow('myObject',int(width/2),height)
    cv2.imshow('myMaskSmall',myMaskSmall)
    cv2.moveWindow('myMaskSmall',0,height)
    cv2.imshow('myMaskSmall2',myMaskSmall2)
    cv2.moveWindow('myMaskSmall2',0,height+int(height/2)+30)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
