from imutils.video import VideoStream
import numpy as np
import cv2
import math
import time
from laser_pointer import LaserPointer
from tkinter import *
from collections import deque


# start video playing
fname = 'Tests/44y.mov'
cap = cv2.VideoCapture(fname)
lower_bound = np.array([156,117,98])
upper_bound = np.array([179,255,255])
fx = open('Repeatability_Tests/44yX.txt','w')
fy = open('Repeatability_Tests/44yY.txt','w')


pointer = LaserPointer(0,0,1,lower_bound,upper_bound)

while(cap.isOpened()):
    ret, frame = cap.read()
    if frame is None:
        break

    cropped_frame = frame[0:720,300:(1280-300),0:3]
    area_measured = pointer.detectDotIntensity(cropped_frame)
    px = pointer.getX()
    py = pointer.getY()

    fx.write(str(px) + '\n')
    fy.write(str(py) + '\n')

    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fx.close()
fy.close()

cap.release()
cv2.destroyAllWindows()
