import numpy as np 

class ConstantForce:
    def __init__(self, c):
        self.c = np.array(c)

    def apply(self, particle, dt):
        return particle.velocity + self.c * dt

class AccelerationForce:
    def __init__(self, a):
        self.a = np.array(a)

    def apply(self, particle, dt):
        return particle.velocity + self.a * dt

class DragForce:
    def __init__(self, vf, b):
        self.vfforce = np.array(vf)
        self.b = b

    def apply(self, particle, dt):
        relative_velocity = particle.velocity - self.vfforce
        drag = -self.b * relative_velocity
        return particle.velocity + drag * dt

class RadialForce:
    def __init__(self, xr, s):
        self.xr = np.array(xr)
        self.s = s

    def apply(self, particle, dt):
        direction = particle.position - self.xr
        distance = np.linalg.norm(direction)
        if distance > 0:
            force = self.s * direction / distance
            return particle.velocity +force * dt