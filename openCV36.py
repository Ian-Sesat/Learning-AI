import cv2
print(cv2.__version__)
width=1280
height=720
class mpPose:
    def __init__(self,tol1=.5,tol2=.5):
        import mediapipe as mp
        self.pose=mp.solutions.pose.Pose(False,False,True,tol1,tol2)
    def poseDataMethod(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        poseData=[]
        results=self.pose.process(frameRGB)
        if results.pose_landmarks != None:
            #print(results.pose_landmarks)
            for lm in results.pose_landmarks.landmark:
                poseData.append((int(lm.x*width),int(lm.y*height)))
            #print(poseData)
        return poseData

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
poseFind=mpPose(.5)
while True:
    ignore, frame=cam.read()
    poseData=poseFind.poseDataMethod(frame)
    cv2.circle(frame,poseData[0],10,(0,255,255),2)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
