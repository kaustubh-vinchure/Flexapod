from serial import Serial
import time
import struct
import numpy as np
from InverseKinematicsConvertors import InverseKinematicsConverter

class MotorController:

    def __init__(self):
        self.port = Serial('COM3',baudrate = 9600, timeout = 10.0)
        time.sleep(5)
        print('Port Opened')
        self.cv = InverseKinematicsConverter([0,0,5.5],0,0,0)


    def close(self):
        self.port.close()


    def write(self,position):
        T = position[0:3]
        psi = position[3]
        phi = position[4]
        theta = position[5]
        T = np.transpose(np.array(T))
        self.cv.updateT(T)
        self.cv.updatePsi(psi)
        self.cv.updatePhi(phi)
        self.cv.updateTheta(theta)

        angles = self.cv.calcAngles()
        package = struct.pack('>BBBBBB',int(angles[0]),int(angles[1]),int(angles[2]),int(angles[3]),int(angles[4]),int(angles[5]))
        self.port.write(package)


if __name__ == '__main__':
    MC = MotorController()
    for i in range(1):
        position = [0,0,5.8,0,1,0]
        MC.write(position)

    MC.close()
