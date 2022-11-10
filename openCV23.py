import cv2
import face_recognition as fr
font=cv2.FONT_HERSHEY_SIMPLEX

donFace=fr.load_image_file('C:/Users/User/Documents/Python/demoImages/known/Donald Trump.jpg')
faceLoc=fr.face_locations(donFace)[0]
donEncode=fr.face_encodings(donFace)[0]

nancyFace=fr.load_image_file('C:/Users/User/Documents/Python/demoImages/known/Nancy Pelosi.jpg')
faceLoc=fr.face_locations(nancyFace)[0]
nancyEncode=fr.face_encodings(nancyFace)[0]

paulFace=fr.load_image_file('C:/Users/User/Documents/Python/demoImages/known/Paul McWhorter.jpg')
faceLoc=fr.face_locations(paulFace)[0]
paulEncode=fr.face_encodings(paulFace)[0]

knownEncodings=[donEncode,nancyEncode,paulEncode]
names=['Donald Trump','Nancy Pelosi','Paul Mcworther']

unknownFaces=fr.load_image_file('C:/Users/User/Documents/Python/demoImages/unknown/u3.jpg')
unKnownFacesBGR=cv2.cvtColor(unknownFaces,cv2.COLOR_RGB2BGR)
faceLocations=fr.face_locations(unknownFaces)
unknownFacesEncodings=fr.face_encodings(unknownFaces,faceLocations)

for faceLocation,unknownFaceEncoding in zip(faceLocations,unknownFacesEncodings):
    top,right,bottom,left=faceLocation
    print(faceLocation)
    cv2.rectangle(unKnownFacesBGR,(left,top),(right,bottom),(0,0,255),2)
    name='Unknown person'
    matches=fr.compare_faces(knownEncodings,unknownFaceEncoding)
    print(matches)
    if True in matches:
        matchIndex=matches.index(True)
        print(matchIndex)
        name=names[matchIndex]
        print(name)
    cv2.putText(unKnownFacesBGR,name,(left,top),font,.75,(0,255,0),2)
cv2.imshow('myWindow',unKnownFacesBGR)
cv2.waitKey(10000)
