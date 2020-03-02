from imutils.video import VideoStream
import numpy as np
import math
import imutils
import cv2
from tkinter import *
import matplotlib

fx = open('20runx.txt','w')
fy = open('20runy.txt','w')


vs = VideoStream(src = 0).start()
slider = Tk()
sensitivity = Scale(slider,from_ = 0, to = 255, orient = HORIZONTAL,length = 400)
sensitivity.pack()
SAMPLING_RATE = 60
samples = 0
while True:
    samples += 1
    slider.update_idletasks()
    slider.update()
    frame = vs.read()
    # gray_frame = cv2.cvtColor(np.uint8(frame),cv2.COLOR_BGR2GRAY)
    # gray_frame = gray_frame.astype('uint8')
    # mean_value = np.mean(gray_frame)
    # std_value = np.std(gray_frame)
    # threshold_value = mean_value + std_value
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(hsv_frame,(11,11),0)
    sens = sensitivity.get()
    lower_white = np.array([0,0,255-sens],dtype = np.uint8)
    upper_white = np.array([255,sens,255],dtype = np.uint8)

    mask = cv2.inRange(blur,lower_white,upper_white)
    # res = cv2.bitwise_and(blur,blur,mask = mask)
    # threshold = cv2.adaptiveThreshold(gray_frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,51,2)
    cv2.imshow('Thresholded Image',mask)
    if samples % SAMPLING_RATE == 0:
        im,cnts,heir = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if(len(cnts) > 0):
            c = max(cnts,key = cv2.contourArea)
            bound_rect = cv2.minAreaRect(c)
            fx.write(str(bound_rect[1][0]) + '\n')
            fy.write(str(bound_rect[1][1]) + '\n')
            bound_box = cv2.boxPoints(bound_rect)
            bound_box = np.int0(bound_box)
            cv2.drawContours(frame,[bound_box],0,(0,0,255),2)
    key = cv2.waitKey(1) & 0xFF
    cv2.imshow('Focal Length Test',frame)
    if key == ord('q'):
        break
fx.close()
fy.close()
vs.stop()
