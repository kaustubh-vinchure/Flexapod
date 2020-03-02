import imutils
from imutils.video import VideoStream
import cv2
import numpy as np
import time

vs = VideoStream(src = 0).start()


while True:
    frame = vs.read()
    blurred = cv2.GaussianBlur(frame,(5,5),0)
    edges = cv2.Canny(blurred,0,100 )

    im, cnts, heir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        c = max(cnts,key = cv2.contourArea)
        x,y,w,h = cv2.boundingRectangle(c)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow('test_distance',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
if not args.get('video',False):
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows
