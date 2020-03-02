from imutils.video import VideoStream
import numpy as np
import cv2
import math
import time
from laser_pointer import LaserPointer
from dot import Dot
from PID import PID
from MotorController import MotorController
from stream_clicker import StreamClicker
# Detect a target dot
fx = open('Accuracy_Test/testholdx.txt','w')
fy = open('Accuracy_Test/testholdy.txt','w')
# adjust for target dot
lower_bound = [110,50,50]
upper_bound = [130,255,255]

targetDot = Dot(0,0,1,lower_bound,upper_bound)
laserPointer = LaserPointer(0,0,1,lower_bound,upper_bound)

x_pid = PID()
y_pid = PID()

motors = MotorController()

dist_est = 4032

x_pid.setKp(1)
x_pid.setKd(0)
x_pid.setKi(0)

y_pid.setKp(1)
y_pid.setKp(0)
y_pid.setKi(0)
position_command = [0,0,5.7,0,0,0]
last_command = position_command
counter = 0

vs = VideoStream(src = 0).start()
frame = vs.read()
frame = frame[240:580,0:520]
cv2.imshow('sugma',frame)
dot_x = []
dot_y = []
# for i in range(30):
#     frame = vs.read()
#     target_area = targetDot.detectDotColor(frame)
#     dot_x.append(targetDot.getX())
#     dot_y.append(targetDot.getY())
# dots_x = np.array(dot_x)
# dots_y = np.array(dot_y)
#
#
# c_x = np.bincount(dots_x)
# c_y = np.bincount(dots_y)
#
# target_x = np.argmax(c_x)
# target_y = np.argmax(c_y)


# target_x = 320
# target_y = 250
dx = 25
dy = 25
sc = StreamClicker(vs)
pixel_pos = sc.getClickEvent()


target_x = pixel_pos[0]
target_y = pixel_pos[1]

motors.write(position_command)

time.sleep(1.5)
frame = vs.read()
frame = frame[240:580,0:520]
laserPointer.detectDotIntensity(frame)
pointer_x_dist_1 = laserPointer.getX()
pointer_y_dist_1 = laserPointer.getY()
print('px',pointer_x_dist_1)
print('py',pointer_y_dist_1)

time.sleep(0.5)

position_command = [0,0,5.7,0,0,3]
motors.write(position_command)

time.sleep(1.5)
frame = vs.read()
frame = frame[240:580,0:520]
laserPointer.detectDotIntensity(frame)
pointer_x_dist_2 = laserPointer.getX()
pointer_y_dist_2 = laserPointer.getY()
print('px',pointer_x_dist_2)
print('py',pointer_y_dist_2)

short_dist = np.sqrt((pointer_x_dist_2-pointer_x_dist_1)**2+(pointer_y_dist_2-pointer_y_dist_1)**2)

dist_est_exp = short_dist/np.tan(np.deg2rad(3))
print('distance estimate',dist_est_exp)

while True:
    frame = vs.read()
    frame = frame[240:580,0:520]
    time.sleep(0.3)
    if frame is None:
        break
    pointer_area = laserPointer.detectDotIntensity(frame)


    pointer_x = laserPointer.getX()
    pointer_y = laserPointer.getY()

    # target_area = targetDot.detectDotColor(frame)
    # dx_old = dx
    # dy_old = dy
    #
    # dx = targetDot.getX()
    # if dx == 0:
    #     dx = dx_old
    # dy = targetDot.getY()
    # if dy == 0:
    #     dy = dy_old

    #frame = frame[abs(pointer_x-90):abs(pointer_x + 90), abs(pointer_y - 90):abs(pointer_y + 90)]
    cv2.imshow('my neighbor',frame)
    cv2.circle(frame,(pointer_x,pointer_y),5,(0,0,255),-1)

    print('px',pointer_x)
    print('py',pointer_y)
    x_pid.update((target_x-pointer_x))
    y_pid.update((target_y-pointer_y))
    new_x = x_pid.getNewVal()
    # new_x = -(target_x - pointer_x) * 0.5
    print('dx',new_x)

    new_y = y_pid.getNewVal()
    # new_y = (target_y - pointer_y) * 0.5
    print('dy',new_y)
    fx.write(str(-new_x)  + '\n')
    fy.write(str(new_y) + '\n')
    # new_x = target_x - pointer_x
    # new_y = target_y - pointer_y
    if abs(new_x) <= 300 and abs(new_y <= 300):
        new_theta = np.rad2deg(np.arctan(new_x/dist_est))
        new_psi = np.rad2deg(np.arctan(new_y/dist_est))

        print('new_theta',new_theta)
        print('new_psi',new_psi)

        # distance.addTheta(new_theta)
        # distance.addPsi(new_psi)
        position_command = [0,0,5.7,0, new_psi,new_theta]

        position_command[4] += last_command[4]
        position_command[5] += last_command[5]
        if np.abs(position_command[4]) > 10 or np.abs(position_command[5]) > 10:
            position_command[4] = 0
            position_command[5] = 0
        print('position',position_command)

        motors.write(position_command)
        last_command = position_command
    key = cv2.waitKey(1) & 10xFF
    if key == ord('q'):
        break


vs.stop()
motors.close()
cv2.destroyAllWindows
