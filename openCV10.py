import cv2
from cv2 import imshow
print(cv2.__version__)
width=640
height=360

snipH=60
snipW=120
boxCR=int(height/2)
boxCC=int(width/2)
deltaRow=1
deltaColumn=1

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore, frame=cam.read()
    frameROI=frame[int(boxCR-snipH/2):int(boxCR+snipH/2),int(boxCC-snipW/2):int(boxCC+snipW/2)]
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
    frame[int(boxCR-snipH/2):int(boxCR+snipH/2),int(boxCC-snipW/2):int(boxCC+snipW/2)]=frameROI
    if int(boxCR-snipH/2)<=0 or int(boxCR+snipH/2)>=height:
        deltaRow=deltaRow*(-1)
    if int(boxCC-snipW/2)<=0 or int(boxCC+snipW/2)>=width:
        deltaColumn=deltaColumn*(-1)
    boxCR=boxCR+deltaRow
    boxCC=boxCC+deltaColumn
    
    cv2.imshow('ROI ',frameROI)
    cv2.moveWindow('ROI ',width,0)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
