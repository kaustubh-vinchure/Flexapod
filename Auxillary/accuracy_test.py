from imutils.video import VideoStream
import numpy as np
import cv2
import math
import time
from laser_pointer import LaserPointer
from tkinter import *
from collections import deque

#start VideoStream
DOT_RADIUS = 1
ACCURACY_SAMPLE_FREQUENCY = 15
TEST_NAME = 'testint2'

x_test_fname = TEST_NAME + 'x.txt'
y_test_fname = TEST_NAME + 'y.txt'

vs = VideoStream(src = 0).start()
lp = LaserPointer(0,0,DOT_RADIUS,0,0)
fx = open(x_test_fname,'w')
fy = open(y_test_fname,'w')
accuracy_time = []
area_expected = DOT_RADIUS**2 * math.pi
frame_counter = 0
t0 = time.time()
lower = Tk()
upper = Tk()
hue_upper = Scale(upper, from_=0, to=179,orient = HORIZONTAL,label = 'Hue Upper',length = 400)
hue_lower = Scale(lower, from_ = 0, to = 179, orient = HORIZONTAL,label = 'Hue Lower',length = 400)
saturation_upper = Scale(upper, from_ = 0, to = 255, orient = HORIZONTAL, label = 'Saturation',length = 400)
saturation_lower = Scale(lower, from_ = 0, to = 255, orient = HORIZONTAL, label = 'Saturation',length = 400)
value_upper = Scale(upper, from_ = 0, to = 255, orient = HORIZONTAL, label = 'Value',length = 400)
value_lower = Scale(lower, from_ = 0, to = 255, orient = HORIZONTAL, label = 'Value',length = 400)
[element.pack() for element in [hue_upper,hue_lower,saturation_lower,saturation_upper,value_upper,value_lower]]
while True:
    frame_counter += 1
    frame = vs.read()
    lower.update_idletasks()
    lower.update()

    upper.update_idletasks()
    upper.update()

    if frame is None:
        break
    upper_bound = [element.get() for element in [hue_upper,saturation_upper,value_upper]]
    lower_bound = [element.get() for element in [hue_lower,saturation_lower,value_lower]]
    upper_bound = [179,255,255]
    lower_bound = [0, 107,107]
    lp.setColor(lower_bound,upper_bound)
    area_measured = lp.detectDotIntensity(frame)

    dotX = lp.getX()
    dotY = lp.getY()
    dotR = lp.getR()
    if frame_counter == ACCURACY_SAMPLE_FREQUENCY:
        frame_counter = 0
        accuracy = area_measured/area_expected
        fx.write(str(dotX) + '\n')
        fy.write(str(dotY) + '\n')


    cv2.circle(frame,(int(dotX),int(dotY)),50,(0,255,255))
    cv2.imshow("Display Laser",frame)
    lower_bgr = cv2.cvtColor(np.uint8([[lower_bound]]),cv2.COLOR_HSV2BGR)
    lower_disp = cv2.resize(lower_bgr,(50,50))

    upper_bgr = cv2.cvtColor(np.uint8([[upper_bound]]),cv2.COLOR_HSV2BGR)
    upper_disp = cv2.resize(upper_bgr,(50,50))


    cv2.imshow('Upper Bound Color',upper_disp)
    cv2.imshow('Lower Bound Color',lower_disp)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
vs.stop()
