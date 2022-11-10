import cv2
print(cv2.__version__)
height=720
width=1280
topVertex=(480,300)
bottomVertex=(800,420)
rectColor=(0,255,0)
rectThickness=-1
circleCenter=(int(width/2),int(height/2))
circleRadius=60
circleColor=(0,0,255)
circleThickness=2
frameText='Ian Sesat'
textPos=(480,300)
textFont=cv2.FONT_HERSHEY_COMPLEX
textScale=1
textColor=(255,0,0)
textThickness=1

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore, frame=cam.read()
    cv2.rectangle(frame,topVertex,bottomVertex,rectColor,rectThickness)
    cv2.circle(frame,circleCenter,circleRadius,circleColor,circleThickness)
    cv2.putText(frame,frameText,textPos,textFont,textScale,textColor,textThickness)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
