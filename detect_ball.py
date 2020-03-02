
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
pts = deque(maxlen = args['buffer'])

if not args.get("video",False):
    vs = VideoStream(src = 0).start()

else:
    vs = cv2.VideoCapture(args['video'])

time.sleep(2.0)

while True:
    frame = vs.read()

    frame = frame[1] if args.get('video',False) else frame

    if frame is None:
        break

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv,lower_blue,upper_blue)


    im,cnts,heir = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        c = max(cnts,key = cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M['m10']/(M['m00']+0.001)), int(M['m01']/(M['m00'] + 0.001)))
        if radius > 2:
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(frame,center,5,(0,0,255),-1)
    pts.appendleft(center)
    for i in range(1,len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(args['buffer']/float(i+1)) * 2.5)
        cv2.line(frame,pts[i-1],pts[i],(0,0,255),thickness)
    cv2.imshow('RIP JUUL',frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
if not args.get('video',False):
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows
