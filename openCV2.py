import cv2
print(cv2.__version__)
cam=cv2.VideoCapture(0)
while True:
    ignore, frame=cam.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    cv2.imshow('grayFrame',gray)
    cv2.moveWindow('grayFrame',640,0) 
    cv2.imshow('myWEBCAM2',frame)
    cv2.moveWindow('myWEBCAM2',640,480)
    cv2.imshow('grayFrame2',gray)
    cv2.moveWindow('grayFrame2',0,480) 
    if cv2.waitKey(1)&0xff == ord('q'):
        break

cam.release()  
