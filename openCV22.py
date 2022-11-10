import cv2
import time

from cv2 import cvtColor
print(cv2.__version__)
width=640
height=360
fpsFILT=30

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
faceCascade=cv2.CascadeClassifier('haar\haarcascade_frontalface_default.xml')
eyeCascade=cv2.CascadeClassifier('haar\haarcascade_eye.xml')
smileCascade=cv2.CascadeClassifier('haar\haarcascade_smile.xml')
pTime=time.time()
time.sleep(.1)

while True:
    ignore, frame=cam.read()
    deltaT=time.time()-pTime
    fps=int(1/deltaT)
    fpsFILT=int(fpsFILT*0.97+fps*0.03)
    print('fps is',fpsFILT)
    pTime=time.time()
    frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(frameGray,1.3,5)
    for face in faces:
        x,y,w,h=face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
        frameROI=frame[y:y+h,x:x+w]
        frameROIGray=cv2.cvtColor(frameROI,cv2.COLOR_BGR2GRAY)
        smiles=smileCascade.detectMultiScale(frameROIGray)
        for smile in smiles:
            xsmile,ysmile,wsmile,hsmile=smile
            cv2.rectangle(frameROI,(xsmile,ysmile),(xsmile+wsmile,ysmile+hsmile),(255,0,0),1)

        eyes=eyeCascade.detectMultiScale(frameROIGray)
        for eye in eyes:
            xeye,yeye,weye,heye=eye
            cv2.rectangle(frame[y:y+h,x:x+w],(xeye,yeye),(xeye+weye,yeye+heye),(0,255,0),1)

    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
