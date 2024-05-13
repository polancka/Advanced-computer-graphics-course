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
            list_emitters.append(PointEmitter(emitter['parameters']['position'], emitter['parameters']['rate'], emitter['particles']['mass'], emitter['particles']['lifetime'], emitter['particles']['velocity']))
        elif emitter['type'] == "disk":
            list_emitters.append(DiskEmitter(emitter['parameters']['position'], emitter['parameters']['radius'],emitter['parameters']['direction'], emitter['parameters']['rate'], emitter['particles']['mass'], emitter['particles']['lifetime'], emitter['particles']['velocity']))
        
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


def run_simulation(emiters, forces):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)

    # Set up the camera
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    x_rotation = y_rotation = 0
    clock = pygame.time.Clock()
    points = []
   
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
                em_x, em_y, em_z = emitter.position
                for _ in range(emitter.rate): 
                    direction = np.random.randn(3)
                    # direction /= np.linalg.norm(direction)  # Normalize the direction vector

                    # Generate a random speed #TODO: change to correct speed
                    speed = random.uniform(0.1, 1.0)

                    # Set the velocity vector
                    velocity = direction * speed

                    # Add the point with initial position (0,0,0) and velocity
                    points.append([em_x, em_y, em_z, velocity[0], velocity[1], velocity[2]])
            else: #radial --> ajdust origin and possible direction
                print("RADIAL not implemented yet")


        for point in points: #TODO: check for removing poitns based on their age based on emitter they came from
            for i in range(3):  # Update x, y, and z coordinates separately
                point[i] += point[i + 3] * dt  # Update position based on velocity
            point[3] = point[3] + dt  # Increment the age of the point by the time since the last frame
            points = [point for point in points if point[3] < 5.0]  # Remove points older than 5 seconds
        
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
        

        # Render points with color based on age
        for point in points:
            age = point[3]
            # Calculate color based on age
            color = (1.0 - age / 5.0, 0.0, 0.0)  # Red component decreases with age
            glColor3f(*color)
                     # Calculate distance from point to the camera
            distance = np.linalg.norm(point[:3])

            # Scale the point size based on distance
            size = 5 / (distance + 1.0)  # Adjust the denominator to control the scale factor
            glPointSize(size)# Set point size
            glBegin(GL_POINTS)
            glVertex3fv(point[:3])  # Render the point
            glEnd()

        pygame.display.flip()


emiters, forces = read_json('01-point.json')
run_simulation(emiters, forces)