import cv2
height=720
width=1280
rows=int(input('Boss, how many rows do you want? '))
columns=int(input('And, how many  columns? '))
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore, frame=cam.read()
    frame=cv2.resize(frame,(int(width/columns),int(height/columns)))
    for i in range(0, rows):
        for j in range(0,columns):
            winName='win'+str(i)+'x'+str(j)
            cv2.imshow(winName,frame)
            cv2.moveWindow(winName,int(width/columns)*j,int(height/columns+30)*i)

    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
