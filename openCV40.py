import cv2
print(cv2.__version__)

class mpHands:
    import mediapipe as mp
    def __init__(self,still=False,numHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(still,numHands,tol1,tol2)
    def marks(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        handsType=[]
        myHands=[]
        if results.multi_hand_landmarks!= None:
            for handLandmarks in results.multi_hand_landmarks:
                myHand=[]
                for landmark in handLandmarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myHands.append(myHand)
            #print(results.multi_handedness)
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                handsType.append(hand.classification[0].label)
        return myHands,handsType

class mpFace:
    import mediapipe as mp
    def __init__(self):
        self.findFace=self.mp.solutions.face_detection.FaceDetection()
    def marks(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        facesData=[]
        results=self.findFace.process(frameRGB)
        if results.detections!=None:
            for face in results.detections:
                #print(face)
                #print(face.location_data.relative_bounding_box)
                bXmin=face.location_data.relative_bounding_box.xmin
                bYmin=face.location_data.relative_bounding_box.ymin
                bHeight=face.location_data.relative_bounding_box.height
                bWidth=face.location_data.relative_bounding_box.width
                topRect=(int(bXmin*width),int(bYmin*height))
                bottomRect=(int((bXmin+bWidth)*width),int((bYmin+bHeight)*height))
                facesData.append((topRect,bottomRect))
        return facesData
class mpPose:
    import mediapipe as mp
    def __init__(self,still=False,halfbody=False,smoothening=True,tol1=.5,tol2=.5):
        self.pose=self.mp.solutions.pose.Pose(still,halfbody,smoothening,tol1,tol2)
    def marks(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        posesData=[]
        results=self.pose.process(frameRGB)
        if results.pose_landmarks!=None:
            #print(results.pose_landmarks)
            #print(results.pose_landmarks.landmark)
            for lm in results.pose_landmarks.landmark:
                #print(lm)
                xPos=int(lm.x*width)
                yPos=int(lm.y*height)
                posesData.append((xPos,yPos))
            #print(posesData)
        return posesData
class mpFaceMeshes:
    import mediapipe as mp
    def __init__(self,still=False,numFaces=3,tol1=.5,tol2=.5,drawMesh=True):
        self.faceMesh=self.mp.solutions.face_mesh.FaceMesh(still,numFaces,tol1,tol2)
        self.mpDraw=self.mp.solutions.drawing_utils
        self.draw=drawMesh
    def marks(self,f):
        frameRGB=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        faceLandMarksData=[]
        results=self.faceMesh.process(frameRGB)
        if results.multi_face_landmarks!=None:
            for facelandmarks in results.multi_face_landmarks:
                myFaceLandmark=[]
                for lm in facelandmarks.landmark:
                    myFaceLandmark.append((int(lm.x*width),int(lm.y*height)))
                faceLandMarksData.append(myFaceLandmark)
                if self.draw==True:
                    self.mpDraw.draw_landmarks(f,facelandmarks,self.mp.solutions.face_mesh.FACE_CONNECTIONS)
        return faceLandMarksData
def myCallBack1(value):
    global lowerLimit
    lowerLimit=value
def myCallBack2(value):
    global upperLimit
    upperLimit=value
                                         
height=720
width=1280
lowerLimit=0
upperLimit=468
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('Trackbars')
cv2.resizeWindow('Trackbars',480,125)
cv2.moveWindow('Trackbars',width,0)
cv2.createTrackbar('lowerLimits','Trackbars',0,468,myCallBack1)
cv2.createTrackbar('upperLimits','Trackbars',468,468,myCallBack2)

findHands=mpHands(numHands=2)
findFaces=mpFace()
findPoses=mpPose()
findFaceMeshes=mpFaceMeshes(drawMesh=False)
while True:
    ignore, frame=cam.read()
    frame=cv2.flip(frame,1)
    faceMeshesData=findFaceMeshes.marks(frame)
    posesData=findPoses.marks(frame)
    facesFound=findFaces.marks(frame)
    myHands,handsType=findHands.marks(frame)
    for face in faceMeshesData:
        indx=0
        for lm in face:
            if indx>= lowerLimit & indx<=upperLimit:
                cv2.putText(frame,str(indx),lm,cv2.FONT_HERSHEY_SIMPLEX,.2,(0,255,0),1)
            indx=indx+1
    for ind in [0,1]:
        cv2.circle(frame,posesData[ind],10,(0,255,255),1)
    for face in facesFound:
        cv2.rectangle(frame,face[0],face[1],(0,0,255),3)

    for hand,handType in zip(myHands,handsType):
        if handType=='Right':
            hType='right'
        if handType == 'Left':
            hType='left'
     
        cv2.putText(frame,hType,hand[8],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()