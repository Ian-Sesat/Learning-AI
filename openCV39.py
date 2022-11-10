import cv2
from cv2 import COLOR_BGR2RGB
import mediapipe as mp

print(cv2.__version__)
height=720
width=1280
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

faceMesh=mp.solutions.face_mesh.FaceMesh()
mpDraw=mp.solutions.drawing_utils
font=cv2.FONT_HERSHEY_COMPLEX
fontColor=(0,255,255)
fontThickness=1
fontScale=.2

drawSpecCircle=mpDraw.DrawingSpec(thickness=1,circle_radius=2,color=(0,0,255))
drawSpecLine=mpDraw.DrawingSpec(thickness=3,circle_radius=2,color=(0,255,0))
while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    frameRGB=cv2.cvtColor(frame,COLOR_BGR2RGB)
    results=faceMesh.process(frameRGB)
    if results.multi_face_landmarks!=None:
        for faceLandmarks in results.multi_face_landmarks:
            #print(faceLandmarks)
            mpDraw.draw_landmarks(frame,faceLandmarks,mp.solutions.face_mesh.FACE_CONNECTIONS,drawSpecCircle,drawSpecLine)
            indx=0
            for lm in faceLandmarks.landmark:
                cv2.putText(frame,str(indx),(int(lm.x*width),int(lm.y*height)),font,fontScale,fontColor,fontThickness)
                indx=indx+1

    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()