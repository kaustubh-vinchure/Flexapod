import serial
import time

class PID:

    def __init__(self,P = 0.1, I = 0.0, D = 0.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sampleTime = 0.00
        self.currentTime = time.time()
        self.lastTime = self.currentTime

        self.setPoint = 0
        self.P = 0
        self.I = 0
        self.D = 0
        self.lastError = 0
        self.output = 0

    def clear(self):
        self.setPoint = 0
        self.P = 0
        self.I = 0
        self.D = 0
        self.lastError = 0
        self.output = 0

    def update(self,feedback):
        error = feedback

        self.currentTime = time.time()
        deltaTime = self.currentTime - self.lastTime
        deltaError = error - self.lastError

        if deltaTime >= self.sampleTime:
            self.P = self.Kp * error
            self.D = 0
            if deltaTime > 0:
                self.D = deltaError/deltaTime * self.Kd
            self.I = error * deltaTime * self.Ki

        self.output = self.P + self.I + self.D

    def getNewVal(self):
        return self.output

    def setKp(self,kp):
        self.Kp = kp

    def setKd(self,kd):
        self.Kd = kd

    def setKi(self,ki):
        self.Ki = ki
