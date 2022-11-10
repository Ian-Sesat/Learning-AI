import pickle 
import cv2
import face_recognition as fr
import os 

print(cv2.__version__)
names=[]
knownEncodings=[]
imageDir='C:/Users/User/Documents/Python/demoImages/known'
for root,dirs,files in os.walk(imageDir):
    for file in files:
        name=file
        name=os.path.splitext(name)[0]
        print(name)
        names.append(name)
        fullFilePath=os.path.join(root,file)
        knownFace=fr.load_image_file(fullFilePath)
        knownEncoding=fr.face_encodings(knownFace)[0]
        knownEncodings.append(knownEncoding)

with open('train.pkl','wb') as f:
    pickle.dump(names,f)
    pickle.dump(knownEncodings,f)  
