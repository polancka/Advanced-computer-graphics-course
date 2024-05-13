
from particle import Particle

class PointEmitter:
    def __init__(self, position, rate, particles_mass, particles_lifetime, particles_velocity):
        self.position = position
        self.rate = rate
        self.time_since_last_emit = 0
        self.particles_mass = particles_mass
        self.particles_lifetime = particles_lifetime
        self.particles_velocity = particles_velocity

    def emit_particles(self, dt):
        # Implement Poisson process sampling here
       pass

    def update(self, dt):
        self.time_since_last_emit += dt
        if self.time_since_last_emit >= 1.0 / self.rate:
            self.emit_particles(dt)
            self.time_since_last_emit = 0

class DiskEmitter:
    def __init__(self, position, radius, direction, rate, particles_mass, particles_lifetime, particles_velocity):
        self.position = position
        self.radius = radius
        self.direction = direction
        self.rate = rate
        self.time_since_last_emit = 0
        self.particles_mass = particles_mass
        self.particles_lifetime = particles_lifetime
        self.particle_velocity = particles_velocity


    def emit_particles(self, dt):
        # Implement Poisson process sampling here
        pass

    def update(self, dt):
        self.time_since_last_emit += dt
        if self.time_since_last_emit >= 1.0 / self.rate:
            self.emit_particles(dt)
            self.time_since_last_emit = 0