import os
import cv2
import face_recognition as fr
print(cv2.__version__)

imageDir='C:/Users/User/Documents/Python/demoImages/known'
for root,dirs,files in os.walk(imageDir):
    print('Root is ',root)
    print('The directories present are: ',dirs)
    print('File names present are: ',files)
    for file in files:
        name=file
        name=os.path.splitext(name)[0]
        print(name)
        fullFilePath=os.path.join(root,file)
        print(fullFilePath)
        myPic=fr.load_image_file(fullFilePath)
        myPicBGR=cv2.cvtColor(myPic,cv2.COLOR_RGB2BGR)
        cv2.imshow(name,myPicBGR)
        cv2.moveWindow(name,0,0)
        cv2.waitKey(2500)
        cv2.destroyAllWindows()
