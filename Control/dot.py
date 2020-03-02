
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
import math
from collections import deque

class Dot:
    COLOR_RANGE_TOLERANCE = 50
    def __init__(self,x,y,r,lower_bound,upper_bound):
        self.x = x
        self.y = y
        self.r = r
        self.lower_bound = np.array(lower_bound)
        self.upper_bound = np.array(upper_bound)
        self.cntR = 0
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getR(self):
        return self.r
    def setColor(self,lower_bound,upper_bound):
        self.upper_bound = np.array(upper_bound)
        self.lower_bound = np.array(lower_bound)
    def detectDotColor(self, frame):
        hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        sharpen_kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
        sharper_frame = cv2.filter2D(hsv_frame,-1,sharpen_kernel)
        mask = cv2.inRange(sharper_frame, self.lower_bound,self.upper_bound)
        #mask = cv2.GaussianBlur(mask,(5,5),0)
        im,cnts,heir = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow('frame',mask)
        if (len(cnts) > 0):
            c = max(cnts,key = cv2.contourArea)
            ((x_circle,y_circle),self.cntR) = cv2.minEnclosingCircle(c)

            M = cv2.moments(c)
            if (M['m00'] > 0):
                self.x = int(M['m10']/M['m00'])
                self.y = int(M['m01']/M['m00'])


        area_measured = self.cntR**2 * math.pi
        return area_measured
    def detectDotIntensity(self,frame):
        gray_frame = cv2.cvtColor(np.uint8(frame),cv2.COLOR_BGR2GRAY)
        gray_frame = gray_frame.astype('uint8')
        blurred_frame = cv2.GaussianBlur(sharper_frame,(5,5),0)
        sharpen_kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
        sharper_frame = cv2.filter2D(blurred_frame,-1,sharpen_kernel)
        ret, threshold = cv2.threshold(sharper_frame,245,255,cv2.THRESH_BINARY)
        cv2.imshow('Thresholded Image',threshold)
        im,cnts,heir = cv2.findContours(threshold.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if (len(cnts) > 0):
            c = max(cnts,key = cv2.contourArea)
            ((x_circle,y_circle),self.cntR) = cv2.minEnclosingCircle(c)

            M = cv2.moments(c)
            if (M['m00'] > 0):
                self.x = int(M['m10']/M['m00'])
                self.y = int(M['m01']/M['m00'])
        return (self.cntR**2 * math.pi)
