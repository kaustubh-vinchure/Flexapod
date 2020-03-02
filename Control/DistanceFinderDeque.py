from collections import deque
import math
import numpy as np


class DistanceFinderDeque:

    def __init__(self,length):
        self.MAX_LENGTH = length
        self.ptsX = deque(maxlen = self.MAX_LENGTH)
        self.ptsY = deque(maxlen = self.MAX_LENGTH)
        self.theta = deque(maxlen = self.MAX_LENGTH)
        self.psi = deque(maxlen = self.MAX_LENGTH)

    def addX(self,x):
        self.ptsX.append(x)

    def addY(self,y):
        self.ptsY.append(y)

    def addTheta(self,theta):
        self.theta.append(theta)

    def addPsi(self,psi):
        self.psi.append(psi)

    def getLength(self):
        xDistance = self.ptsX[0] - self.ptsX[-1]
        yDistance = self.ptsY[0] - self.ptsY[-1]

        xRotation = self.theta[0] - self.theta[-1]
        yRotation = self.psi[0] - self.psi[-1]

        dy = xDistance/np.tan(np.deg2rad(yRotation))
        dx = yDistance/np.tan(np.deg2rad(xRotation))

        distance = (dy + dx)/2

        return distance
