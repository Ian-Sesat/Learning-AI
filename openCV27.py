import face_recognition as fr
import cv2
import pickle

print(cv2.__version__)
font=cv2.FONT_HERSHEY_SIMPLEX
height=720
width=1280
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

with open('train.pkl', 'rb') as f:
    names=pickle.load(f)
    knownEncodings=pickle.load(f)

while True:
    ignore, myPicture=cam.read()
    myPictureRGB=cv2.cvtColor(myPicture,cv2.COLOR_BGR2RGB)
    faceLocations=fr.face_locations(myPictureRGB)
    unKnownEncodings=fr.face_encodings(myPictureRGB,faceLocations)

    for faceLocation,unknownEncoding in zip(faceLocations,unKnownEncodings):
        top,right,bottom,left=faceLocation
        cv2.rectangle(myPicture,(left,top),(right,bottom),(0,0,255),2)
        name='unknown person'
        matches=fr.compare_faces(knownEncodings,unknownEncoding)
        if True in matches:
            matchIndex=matches.index(True)
            name=names[matchIndex]
        cv2.putText(myPicture,name,(left,top),font,.75,(255,0,0),2)

    cv2.imshow('myWEBCAM',myPicture)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

