import cv2
import time

print(cv2.__version__)
height=720
width=1280
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
fpsFILT=30
tlast=time.time()
time.sleep(.1)
while True:
    ignore, frame=cam.read()
    dT=time.time()-tlast
    fps=1/dT
    fpsFILT=int(fpsFILT*0.97+fps*0.03)
    tlast=time.time()
    cv2.rectangle(frame,(0,0),(125,40),(255,0,255),-1)
    cv2.putText(frame,str(fpsFILT)+' fps',(0,25),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
    cv2.imshow('myWEBCAM', frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()