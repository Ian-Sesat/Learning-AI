import cv2
print(cv2.__version__)
import numpy as np
checkerSize=int(input('Boss, what size do you want your checker board to be? '))
numSquares=int(input('And how many squares per row and column? '))
squareSize=int(checkerSize/numSquares)

darkColor=(0,0,0)
lightColor=(0,0,255)
nowColor=darkColor

while True:
    frame=np.zeros([checkerSize,checkerSize,3],dtype=np.uint8)
    for i in range(0,numSquares):
        for j in range(0,numSquares):
            frame[squareSize*i:squareSize*(i+1),squareSize*j:squareSize*(j+1)]=nowColor
            if nowColor==darkColor:
                nowColor=lightColor
            else:
                nowColor=darkColor
        if nowColor==darkColor:
            nowColor=lightColor
        else:
            nowColor=darkColor
    cv2.imshow('CheckerBoard',frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break









