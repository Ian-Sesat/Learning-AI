#Super fast face detection with mediapipe
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

findFaces=mp.solutions.face_detection.FaceDetection()
mpDraw=mp.solutions.drawing_utils

while True:
    ignore, frame=cam.read()
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=findFaces.process(frameRGB)
    if results.detections!= None:
        #print(results.detections)
        for face in results.detections:
            #mpDraw.draw_detection(frame,face)
            #print(face.location_data)
            #print(face.location_data.relative_bounding_box)
            xMin=face.location_data.relative_bounding_box.xmin
            yMin=face.location_data.relative_bounding_box.ymin
            rectWidth=face.location_data.relative_bounding_box.width
            rectHeight=face.location_data.relative_bounding_box.height
            topLeft=(int(xMin*width),int(yMin*height))
            bottomRight=(int((xMin+rectWidth)*width),int((yMin+rectHeight)*height))
            cv2.rectangle(frame,topLeft,bottomRight,(0,0,255),3)

    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()