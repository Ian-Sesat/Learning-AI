import cv2
import face_recognition as fr

font=cv2.FONT_HERSHEY_SIMPLEX
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

ianFace=fr.load_image_file('C:/Users/User/Documents/Python/demoImages/known/Ian Sesat.jpg')
faceLoc=fr.face_locations(ianFace)[0]
ianEncodings=fr.face_encodings(ianFace)[0]

mosesFace=fr.load_image_file('C:/Users/User/Documents/Python/demoImages/known/Moses Mwangi.jpg')
faceLoc=fr.face_locations(mosesFace)[0]
mosesEncodings=fr.face_encodings(mosesFace)[0]


knownEncodings=[ianEncodings,mosesEncodings]
names=['Ian Sesat','Moses Mwangi']

while True:
    ignore, unknownFace=cam.read()
    unknownFaceRGB=cv2.cvtColor(unknownFace,cv2.COLOR_BGR2RGB)
    faceLocations=fr.face_locations(unknownFaceRGB)
    unknownEncodings=fr.face_encodings(unknownFaceRGB)

    for faceLocation,unknownEncoding in zip(faceLocations,unknownEncodings):
        top,right,bottom,left=faceLocation
        print(faceLocation)
        cv2.rectangle(unknownFace,(left,top),(right,bottom),(0,0,255),2)
        name='Unknown Person'
        matches=fr.compare_faces(knownEncodings,unknownEncoding)
        if True in matches:
            matchIndex=matches.index(True)
            print(matchIndex)
            name=names[matchIndex]
            print(name)
        cv2.putText(unknownFace,name,(left,top),font,.75,(0,255,0),2)
    
    cv2.imshow('myWEBCAM',unknownFace)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
