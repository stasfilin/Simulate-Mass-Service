

import math
import random
import sys

MAX_SIZE = sys.maxsize

class MassService:
    lya = 0.0
    n = 3
    r = 4
    myu = {}
    L = {}
    lmean = {}
    lmax = 0
    K = {}
    T = {}
    Tnext = 0.0
    t = 0.0
    Tmod = 1000
    refusals = 0
    served = 0
    def __init__(self):
        j = 0

        self.Tmod = 1000
        self.lya = 1.0
        self.myu = [2.0, 0.5, 0.5, 2.0]
        self.lmax = 1
        while j < self.r:
            self.K[j] = 0
            self.T[j] = MAX_SIZE
            j+=1
        i = 0
        while i<self.n:
            self.L[i] = 0
            self.lmean[i] = 0.0
            i+=1

    def event0(self):
        if self.K[0] == 0:
            self.K[0] = 1
            self.T[0] = float(self.t + float((-1 / self.myu[0] * math.log(random.random()))))
        else:
            self.refusals+=1
        self.Tnext = float(self.t + float((-1 / self.lya * math.log(random.random()))))

    def event1(self):
        self.K[0] = 0
        self.T[0] = MAX_SIZE
        if self.K[1] == 0:
            self.K[1] = 1
            self.T[1] = float(self.t + float((-1 / self.myu[1] * math.log(random.random()))))
        elif self.K[2] == 0:
            self.K[2] = 1
            self.T[2] = float(self.t + float((-1 / self.myu[2] * math.log(random.random()))))
        else:
            self.L[1]+=1
    def event2and3(self, k):
        if self.L[2] == self.lmax:
            self.K[k] = 2
            self.T[k] = MAX_SIZE
        else:
            self.K[k] = 0
            self.T[k] = MAX_SIZE
            if self.L[1] > 0:
                self.L[1]-=1
                self.K[k] = 1
                self.T[k] = float(self.t + float((-1 / self.myu[k] * math.log(random.random()))))
            if self.K[3] == 0:
                self.K[3] = 1
                self.T[3] = float(self.t + float((-1 / self.myu[3] * math.log(random.random()))))
            else:
                self.L[2]+=1
    def event4(self):
        self.served+=1
        self.K[3] = 0
        self.T[3] = MAX_SIZE
        if self.L[2] > 0:
            self.L[2]-=1
            self.K[3] = 1
            self.T[3] = float(self.t + float((-1 / self.myu[3] * math.log(random.random()))))
        if self.K[1] == 2:
            self.event2and3(1)
        if self.K[2] == 2:
            self.event2and3(2)

    def go(self):
        self.t = 0.0
        self.tmin = 0.0
        self.event = 0
        while self.t < self.Tmod:
            self.tmin = self.Tnext
            self.event = 0
            j1 = 0
            while j1 < self.r:
                if self.T[j1] < self.tmin:
                    self.tmin = self.T[j1]
                    self.event = j1+1
                j1+=1
            j2 = 0
            while j2 <self.n:
                self.lmean[j2] += float(self.L[j2] * (self.tmin - self.t))
                j2+=1
            self.t = self.tmin
            if self.event == 0:
                self.event0()
            if self.event == 1:
                self.event1()
            if self.event == 2:
                self.event2and3(1)
            if self.event == 3:
                self.event2and3(2)
            if self.event == 4:
                self.event4()
        print "refusals = "+str(self.refusals) + "\nserved = "+str(self.served)
        print "L1 = "+str(self.L[1])
        print "L2 = "+str(self.L[2])
        print "lmean1 = "+str(self.lmean[1]/self.Tmod)
        print "lmean1 = "+str(self.lmean[2]/self.Tmod)

MassService().go()