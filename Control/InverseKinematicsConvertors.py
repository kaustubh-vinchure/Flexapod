import numpy as np

class InverseKinematicsConverter:


    def __init__(self,T, psi, phi, theta):
        self.psi = np.deg2rad(psi)
        self.phi = np.deg2rad(phi)
        self.theta = np.deg2rad(theta)
        self.T = T

        self.rb = np.array([[np.cos(self.psi) * np.cos(self.theta),
        -np.sin(self.psi) * np.cos(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        np.sin(self.psi) * np.sin(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [np.sin(self.psi)*np.cos(self.theta),
        np.cos(self.psi)*np.cos(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        -np.cos(self.psi) * np.sin(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [-np.sin(self.theta),
        np.cos(self.theta) * np.sin(self.phi),
        np.cos(self.theta) * np.cos(self.phi)
        ]])


        self.a_1 = 4.41
        self.b_1 = 0.76
        self.a_2 = 4.67
        self.b_2 = 1.55
        self.la = 6
        self.lb = 0.4

    def calcP(self):
        self.p1 = np.transpose(np.array([self.b_1,-self.a_1 * np.sqrt(3)/2,0]))
        # print('p1',self.p1)
        self.p2 = np.transpose(np.array([self.a_1 - np.cos(np.deg2rad(60)) * (self.a_1/2-self.b_1),
        (self.a_1/2 - self.b_1) * np.sin(np.deg2rad(60)),0]))
        # print('p2',self.p2)
        self.p3 = np.transpose(np.array([self.a_1 - np.cos(np.deg2rad(60)) * (self.a_1/2+self.b_1),
        (self.a_1/2 + self.b_1) * np.sin(np.deg2rad(60)),0]))
        # print('p3',self.p3)
        self.p4 = np.transpose(np.array([-self.a_1 + np.cos(np.deg2rad(60)) * (self.a_1/2 + self.b_1),
        (self.a_1/2 + self.b_1) * np.sin(np.deg2rad(60)),0]))
        # print('p4',self.p4)
        self.p5 = np.transpose(np.array([-self.a_1 + np.cos(np.deg2rad(60)) * (self.a_1/2 - self.b_1),
        (self.a_1/2 - self.b_1) * np.sin(np.deg2rad(60)),0]))
        # print('p5',self.p5)
        self.p6 = np.transpose(np.array([-self.b_1,-self.a_1 * np.sqrt(3)/2,0]))
        # print('p6',self.p6)

    def calcB(self):
        self.b1 = np.array([self.a_2 - np.cos(np.deg2rad(60)) * (self.a_2/2 + self.b_2),
        -np.sin(np.deg2rad(60)) * (self.a_2/2 + self.b_2),0])
        # print('b1',self.b1)
        self.b2 = np.array([self.a_2 - np.cos(np.deg2rad(60)) * (self.a_2/2 - self.b_2),
        -np.sin(np.deg2rad(60)) * (self.a_2/2 - self.b_2),0])
        # print('b2',self.b2)
        self.b3 = np.array([self.b_2,self.a_2 * np.sqrt(3)/2,0])
        # print('b3',self.b3)
        self.b4 = np.array([-self.b_2,self.a_2 * np.sqrt(3)/2,0])
        # print('b4',self.b4)
        self.b5 = np.array([-self.a_2 + np.cos(np.deg2rad(60)) * (self.a_2/2 - self.b_2),
        -np.sin(np.deg2rad(60)) * (self.a_2/2 - self.b_2),0])
        # print('b5',self.b5)
        self.b6 = np.array([-self.a_2 + np.cos(np.deg2rad(60)) * (self.a_2/2 + self.b_2),
        -np.sin(np.deg2rad(60)) * (self.a_2/2 + self.b_2),0])
        # print('b6',self.b6)

    def calcK(self):
        self.k1 = self.T + self.rb @ self.p1 - self.b1
        self.k2 = self.T + self.rb @ self.p2 - self.b2
        self.k3 = self.T + self.rb @ self.p3 - self.b3
        self.k4 = self.T + self.rb @ self.p4 - self.b4
        self.k5 = self.T + self.rb @ self.p5 - self.b5
        self.k6 = self.T + self.rb @ self.p6 - self.b6

        self.k_1 = np.linalg.norm(self.k1)
        self.k_2 = np.linalg.norm(self.k2)
        self.k_3 = np.linalg.norm(self.k3)
        self.k_4 = np.linalg.norm(self.k4)
        self.k_5 = np.linalg.norm(self.k5)
        self.k_6 = np.linalg.norm(self.k6)

        # print('k1',self.k_1)
        # print('k2',self.k_2)
        # print('k3',self.k_3)
        # print('k4',self.k_4)
        # print('k5',self.k_5)
        # print('k6',self.k_6)


    def calcAngles(self):
        self.calcP()
        self.calcB()
        self.calcK()

        cons1 = (self.la**2 - self.k_1**2 - self.lb**2)/-2
        cons2 = (self.la**2 - self.k_2**2 - self.lb**2)/-2
        cons3 = (self.la**2 - self.k_3**2 - self.lb**2)/-2
        cons4 = (self.la**2 - self.k_4**2 - self.lb**2)/-2
        cons5 = (self.la**2 - self.k_5**2 - self.lb**2)/-2
        cons6 = (self.la**2 - self.k_6**2 - self.lb**2)/-2

        xvec = np.linspace(-np.pi/2,np.pi/2,100)

        lb12x = self.lb * np.cos(xvec) * np.cos(np.deg2rad(60))
        lb12y = self.lb * np.cos(xvec) * np.sin(np.deg2rad(60))
        lb56x = self.lb * np.cos(xvec) * np.cos(np.deg2rad(60))
        lb56y = -self.lb * np.cos(xvec) * np.sin(np.deg2rad(60))
        lb34x = -self.lb * np.cos(xvec) * np.sin(np.deg2rad(60))
        lb34y = 0 * xvec


        lbz = self.lb * np.sin(xvec)
        leg1 = self.k1[0] * lb12x + self.k1[1] * lb12y + self.k1[2] * lbz
        leg2 = self.k2[0] * lb12x + self.k2[1] * lb12y + self.k2[2] * lbz
        leg3 = self.k3[0] * lb34x + self.k3[1] * lb34y + self.k3[2] * lbz
        leg4 = self.k4[0] * lb34x + self.k4[1] * lb34y + self.k4[2] * lbz
        leg5 = self.k5[0] * lb56x + self.k5[1] * lb56y + self.k5[2] * lbz
        leg6 = self.k6[0] * lb56x + self.k6[1] * lb56y + self.k6[2] * lbz

        idx1 = np.argmin(np.abs(leg1-cons1))
        idx2 = np.argmin(np.abs(leg2-cons2))
        idx3 = np.argmin(np.abs(leg3-cons3))
        idx4 = np.argmin(np.abs(leg4-cons4))
        idx5 = np.argmin(np.abs(leg5-cons5))
        idx6 = np.argmin(np.abs(leg6-cons6))

        beta1 = xvec[idx1]
        beta2 = xvec[idx2]
        beta3 = xvec[idx3]
        beta4 = xvec[idx4]
        beta5 = xvec[idx5]
        beta6 = xvec[idx6]


        ang1 = np.rad2deg(beta1 + np.pi/2 - np.deg2rad(6))*(180/156)
        ang2 = (np.rad2deg(beta2 + np.pi/2) - 7) * (180/164)
        ang3 = (np.rad2deg(beta3 + np.pi/2) - 2)  * (180/158)
        ang4 = np.rad2deg(beta4 + np.pi/2) * (180/160)
        ang5 = (np.rad2deg(beta5 + np.pi/2) - 6) * (180/160)
        ang6 = (np.rad2deg(beta6 + np.pi/2) - 2) * (180/163)

        lis = [ang1,ang2,ang3,ang4,ang5,ang6]
        for idx,ang in enumerate(lis):
            if ang <= 0:
                lis[idx] = 0
            elif ang > 180:
                lis[idx] = 180

        return lis

    def updateT(self,T):
        self.T = T

    def updatePsi(self,psi):
        self.psi = np.deg2rad(psi)

        self.rb = np.array([[np.cos(self.psi) * np.cos(self.theta),
        -np.sin(self.psi) * np.cos(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        np.sin(self.psi) * np.sin(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [np.sin(self.psi)*np.cos(self.theta),
        np.cos(self.psi)*np.cos(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        -np.cos(self.psi) * np.sin(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [-np.sin(self.theta),
        np.cos(self.theta) * np.sin(self.phi),
        np.cos(self.theta) * np.cos(self.phi)
        ]])


    def updatePhi(self,phi):
        self.phi = np.deg2rad(phi)


        self.rb = np.array([[np.cos(self.psi) * np.cos(self.theta),
        -np.sin(self.psi) * np.cos(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        np.sin(self.psi) * np.sin(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [np.sin(self.psi)*np.cos(self.theta),
        np.cos(self.psi)*np.cos(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        -np.cos(self.psi) * np.sin(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [-np.sin(self.theta),
        np.cos(self.theta) * np.sin(self.phi),
        np.cos(self.theta) * np.cos(self.phi)
        ]])

    def updateTheta(self,theta):
        self.theta = np.deg2rad(theta)


        self.rb = np.array([[np.cos(self.psi) * np.cos(self.theta),
        -np.sin(self.psi) * np.cos(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        np.sin(self.psi) * np.sin(self.phi) + np.cos(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [np.sin(self.psi)*np.cos(self.theta),
        np.cos(self.psi)*np.cos(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.sin(self.phi),
        -np.cos(self.psi) * np.sin(self.phi) + np.sin(self.psi) * np.sin(self.theta) * np.cos(self.phi)],
        [-np.sin(self.theta),
        np.cos(self.theta) * np.sin(self.phi),
        np.cos(self.theta) * np.cos(self.phi)
        ]])



if __name__ == '__main__':
    T = np.array([0,0,5.8])
    T = np.transpose(T)
    phi = 0
    psi = 0
    theta = 3
    converter = InverseKinematicsConverter(T,psi,phi,theta)
    angles = converter.calcAngles()
    print(angles)
