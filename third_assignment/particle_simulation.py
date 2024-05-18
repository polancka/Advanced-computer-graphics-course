import json
import pygame
import time
import sys
import random
import numpy as np
from pygame.locals import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from particle import Particle
from forces import ConstantForce, DragForce, AccelerationForce,RadialForce
from emitter import PointEmitter, DiskEmitter
from math import pi, cos, sin

#reads the json file and append instances of correct classes with all additional info
def read_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)

    emitters = data['emitters']
    forces = data['forces']
    list_emitters = []
    list_forces = []

    for emitter in emitters:
        if emitter['type'] == "point":
            list_emitters.append(PointEmitter(emitter['parameters']['position'], emitter['parameters']['rate'], emitter['particles']['mass'], emitter['particles']['lifetime'][0], emitter['particles']['lifetime'][1],emitter['particles']['velocity']))
        elif emitter['type'] == "disk":
            list_emitters.append(DiskEmitter(emitter['parameters']['position'], emitter['parameters']['radius'],emitter['parameters']['direction'], emitter['parameters']['rate'], emitter['particles']['mass'], emitter['particles']['lifetime'][0], emitter['particles']['lifetime'][1], emitter['particles']['velocity']))
        
    for force in forces:
        if force['type'] == "drag": 
            list_forces.append(DragForce(force['parameters']['wind'], force['parameters']['drag']))
        elif force['type'] == "acceleration": 
            list_forces.append(AccelerationForce(force['parameters']['acceleration']))
        elif force['type'] == "constant": 
            list_forces.append(ConstantForce(force['parameters']['force']))
        elif force['type'] == "radial": 
            list_forces.append(RadialForce(force['parameters']['position'], force['parameters']['strength']))


    return list_emitters, list_forces

def draw_disk(center, radius, segments):
    """ Draw a disk centered at `center` with given `radius` and `segments` """
    # Start drawing a triangle fan
    glBegin(GL_TRIANGLE_FAN)

    # Set the center of the disk
    glVertex3f(center[0], center[1], center[2])

    # Create points around the circle
    for i in range(segments + 1):  # +1 to close the circle
        angle = 2 * pi * i / segments
        x = center[0] + radius * cos(angle)
        y = center[1] + radius * sin(angle)
        z = center[2]  # Disk lies in the XY plane, so z is constant
        glVertex3f(x, y, z)

    glEnd()

def run_simulation(emiters, forces):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)

    # Set up the camera
    gluPerspective(60, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(7, 3, -10)

    x_rotation = y_rotation = 0
    clock = pygame.time.Clock()
    particles = []

    time_interval = 1.0
   
    # Main loop
    while True: #TODO: add forces and updating the points

        dt = clock.tick(60) / 1000.0 #TODO: replace this with Poisson

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            y_rotation -= 1
        if keys[pygame.K_RIGHT]:
            y_rotation += 1
        if keys[pygame.K_UP]:
            x_rotation -= 1
        if keys[pygame.K_DOWN]:
            x_rotation += 1
        
        for emitter in emiters: 
            if isinstance(emitter, PointEmitter):
                time_elapsed = 0
                while time_elapsed < time_interval:
                    # Generate the next emission time using exponential distribution
                    delta_t = -np.log(1 - random.random()) / emitter.rate
                    time_elapsed += delta_t
                    
                    if time_elapsed < time_interval: 
                        em_x, em_y, em_z = emitter.position
                        
                        direction = np.random.randn(3)
                        speed = random.uniform(0.1, 1.0)

                        # Set the velocity vector
                        velocity = direction * speed
                        particle = Particle(emitter, velocity)
                        particles.append(particle)
                        # points.append([em_x, em_y, em_z, velocity[0], velocity[1], velocity[2], 0.0])
            elif isinstance(emitter, DiskEmitter):
                time_elapsed = 0
                while time_elapsed < time_interval:
                    delta_t = -np.log(1 - random.random()) / emitter.rate
                    time_elapsed += delta_t
                    
                    if time_elapsed < time_interval: 
                        em_x, em_y, em_z = emitter.position  
                        em_x = em_x + random.uniform(-emitter.radius/2, emitter.radius/2)
                        em_y = em_y + random.uniform(-emitter.radius/2, emitter.radius/2)
                        
                        opposite_vector = [- component for component in emitter.direction]
                        direction = random.choice([opposite_vector, emitter.direction])
                        speed = 1

                        # Set the velocity vector
                        velocity = direction * speed
                        particle = Particle(emitter, velocity)
                        particles.append(particle)
                        # points.append([em_x, em_y, em_z, velocity[0], velocity[1], velocity[2], 0.0])
            


        # new_points = []
        # for point in points:
        #     for force in forces:
        #         point[3] += force[0] * dt  # Apply force to velocity x
        #         point[4] += force[1] * dt  # Apply force to velocity y
        #         point[5] += force[2] * dt  # Apply force to velocity z

        #     # Update position based on velocity
        #     for i in range(3):
        #         point[i] += point[i + 3] * dt
           
        #     point[6] += dt  # Increment age
        #     if point[6] < 0.8:  # Keep points younger than 5 seconds
        #         new_points.append(point)
        # points = new_points

        # Update particles with forces
        new_particles = []
        for particle in particles:
            particle.update(dt, forces)
            if particle.age < particle.lifetime:
                new_particles.append(particle)
        particles = new_particles
        
        # Clear the screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()  # Reset the view

        # Apply rotations based on keyboard input
        glRotatef(x_rotation, 1, 0, 0)
        glRotatef(y_rotation, 0, 1, 0)

        # Render coordinate axes
        glBegin(GL_LINES)
        # x-axis (red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-5.0, 0.0, 0.0)
        glVertex3f(5.0, 0.0, 0.0)
        # y-axis (green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, -5.0, 0.0)
        glVertex3f(0.0, 5.0, 0.0)
        # z-axis (blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, -5.0)
        glVertex3f(0.0, 0.0, 5.0)
        glEnd() 

        for emitter in emiters: 
            if isinstance(emitter, DiskEmitter):
                glColor3f(1, 1, 0)  # Set disk color to red
                draw_disk(emitter.position, emitter.radius/2, 32)
        

        # Render points with color based on age
        for particle in particles:
            # age = point[3]
            # # Calculate color based on age
            # color = (1.0 , 0.0 + age / 5.0, 0.0)  # Red component decreases with age
            # glColor3f(*color)
            #          # Calculate distance from point to the camera
            # distance = np.linalg.norm(point[:3])

            # # Scale the point size based on distance
            # size = 5 / (distance + 1.0)  # Adjust the denominator to control the scale factor
            # glPointSize(size)# Set point size
            # glBegin(GL_POINTS)
            # glVertex3fv(point[:3])  # Render the point
            # glEnd()
            age = particle.age
            color = (1.0, age / 1.5, 0.0)  # Red component decreases with age
            glColor3f(*color)
            distance = np.linalg.norm(particle.position)
            size = 5 / (distance + 1.0)
            glPointSize(size)
            glBegin(GL_POINTS)
            glVertex3fv(particle.position)
            glEnd()

        pygame.display.flip()

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == '2': 
            emiters, forces = read_json('02-disk.json')
        elif arg == '3': 
            emiters, forces = read_json('03-radial.json')
        elif arg == '4': 
            emiters, forces = read_json('04-constant.json')
        elif arg == '5': 
            emiters, forces = read_json('05-masses.json')
        elif arg == '6': 
            emiters, forces = read_json('06-stress.json')
    else:
        emiters, forces = read_json('01-point.json')

    for force in forces:
        print(force)

  
    run_simulation(emiters, forces)

if __name__ == "__main__":
    main()

