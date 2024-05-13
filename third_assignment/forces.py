import numpy as np 

class ConstantForce:
    def __init__(self, c):
        self.c = np.array(c)

    def calculate(self, particle):
        return self.force

class AccelerationForce:
    def __init__(self, a):
        self.a = np.array(a)

    def calculate(self, particle):
        return particle.mass * self.a

class DragForce:
    def __init__(self, vf, b):
        self.vf = np.array(vf)
        self.b = b

    def calculate(self, particle):
        return -self.b * (particle.velocity - self.vf)

class RadialForce:
    def __init__(self, xr, s):
        self.xr = np.array(xr)
        self.s = s

    def calculate(self, particle):
        r = particle.position - self.xr
        return -self.s * r / np.linalg.norm(r)**3