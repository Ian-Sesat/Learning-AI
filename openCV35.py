import cv2
import mediapipe as mp

print(cv2.__version__)
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

#creating the mediapipe pose and drawing objects:
pose=mp.solutions.pose.Pose(False,False,True,.5,.5)
mpDrawing=mp.solutions.drawing_utils

while True:
    ignore, frame=cam.read()
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=pose.process(frameRGB)
    #print(results)
    myPoseLandMarks=[]
    if results.pose_landmarks != None:
        #print(results.pose_landmarks)
        #print(results.pose_landmarks.landmark)
        for lm in results.pose_landmarks.landmark:
            #print((int(lm.x*width),int(lm.y*height)))
            myPoseLandMarks.append((int(lm.x*width),int(lm.y*height)))
        cv2.circle(frame,myPoseLandMarks[0],10,(0,0,255),3)
        cv2.circle(frame,myPoseLandMarks[2],5,(255,0,0),-1)
        cv2.circle(frame,myPoseLandMarks[5],5,(255,0,0),-1)

        #mpDrawing.draw_landmarks(frame,results.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',200,200)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()