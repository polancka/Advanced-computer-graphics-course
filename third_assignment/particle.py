import numpy as np
import random
from emitter import DiskEmitter

class Particle:
    def __init__(self, emitter, velocity):
        if isinstance(emitter, DiskEmitter):
            em_x, em_y, em_z = emitter.position  
            em_x = em_x + random.uniform(-emitter.radius/2, emitter.radius/2)
            em_y = em_y + random.uniform(-emitter.radius/2, emitter.radius/2)
            self.position = np.array([em_x, em_y, em_z])
        else: 
            self.position = np.array(emitter.position, dtype=np.float64)
        self.velocity = velocity
        self.mass = emitter.particles_mass
        self.lifetime = random.uniform(emitter.particles_lifetime_a, emitter.particles_lifetime_b)
        self.age = 0

    def update(self, dt, forces):
        velocities = []
        for force in forces:
            new_velocity = force.apply(self, dt)
            velocities.append(new_velocity)
        # Convert the list of tuples/lists into a NumPy array
        vector_array = np.array(velocities)

        # Sum the vectors
        sum_of_vectors = np.sum(vector_array, axis=0)
        self.velocity = sum_of_vectors
        self.position += self.velocity * dt
        self.age += dt