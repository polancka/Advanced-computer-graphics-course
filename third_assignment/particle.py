import numpy as np

class Particle:
    def __init__(self, emitter):
        self.position = np.array(emitter.position, dtype=np.float64)
        self.velocity = np.array(emitter.particles_velocity, dtype=np.float64)
        self.mass = emitter.particles_mass
        self.lifetime = emitter.particles_lifetime
        self.alive = True

    def update(self, dt, forces):
        if self.lifetime > 0:
            acceleration = sum([force.calculate(self) for force in forces], np.array([0,0,0])) / self.mass
            self.velocity += acceleration * dt
            self.position += self.velocity * dt
            self.lifetime -= dt
        else:
            self.alive = False