import cv2
print(cv2.__version__)
width=640
height=360
evt=0
def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global pnt
    if event==cv2.EVENT_LBUTTONDOWN:
        print('Mouse event was: ',event)
        print('at position',xPos,yPos)
        evt=event
        pnt=(xPos,yPos)
    if event==cv2.EVENT_LBUTTONUP:
        print('Mouse event was: ',event)
        print('at position: ',xPos,yPos)
        evt=event
        pnt=(xPos,yPos)
    if event==cv2.EVENT_RBUTTONUP:
        print('Mouse event was: ',event)
        print('at position',xPos,yPos)
        evt=event

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myWEBCAM')
cv2.setMouseCallback('myWEBCAM', mouseClick)

while True:
    ignore, frame=cam.read()
    if evt==1 or evt==4:
        cv2.circle(frame,pnt,25,(0,255,0),2)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
