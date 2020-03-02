from imutils.video import VideoStream
import numpy as np
import cv2
import math
import time
from laser_pointer import LaserPointer
from tkinter import *
from collections import deque


# start video playing
fname = 'Tests/Hexapod.mov'
cap = cv2.VideoCapture(fname)
lower_bound = np.array([156,117,98])
upper_bound = np.array([179,255,255])
fx = open('Repeatability_Tests/circleX.txt','w')
fy = open('Repeatability_Tests/circleY.txt','w')


pointer = LaserPointer(0,0,1,lower_bound,upper_bound)

while(cap.isOpened()):
    ret, frame = cap.read()
    if frame is None:
        break
    area_measured = pointer.detectDotIntensity(frame)
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
