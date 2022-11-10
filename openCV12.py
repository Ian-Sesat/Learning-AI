from ssl import PROTOCOL_TLSv1_1
import cv2
print(cv2.__version__)
width=640
height=360
evt=0
def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global pt1
    global pt2
    if event==cv2.EVENT_LBUTTONDOWN:
        print(event)
        evt=event
        pt1=(xPos,yPos)
    if event==cv2.EVENT_LBUTTONUP:
        print(event)
        evt=event
        pt2=(xPos,yPos)
    if event==cv2.EVENT_RBUTTONUP:
        print(event)
        evt=event

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myWEBCAM')
cv2.setMouseCallback('myWEBCAM',mouseClick)
while True:
    ignore, frame=cam.read()
    if evt==4:
        cv2.rectangle(frame,pt1,pt2,(0,255,0),2)
        ROI=frame[pt1[1]:pt2[1],pt1[0]:pt2[0]]
        cv2.imshow('ROI',ROI)
        cv2.moveWindow('ROI',width+10,0)
    if evt==5:
        cv2.destroyWindow('ROI')
        evt=0
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
