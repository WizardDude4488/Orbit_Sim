#importing the libraries

import pygame
import math
import numpy as np
import array


#creating some variables for setting up the screen
SCREEN_Width = 1280
SCREEN_Height = 720
SCREEN_Size = (SCREEN_Width, SCREEN_Height)

#FPS for game loop
FPS = 120

#setting the mode of the display
pygame.init()
screen = pygame.display.set_mode(SCREEN_Size)
pygame.display.update()

#define universal constant of gravitation, G
global G
G = 6.67430 * (10 ** -11)

class Calculations:
    #make some object properties so the program can store values while calculating
    def __init__(self, stat_mass, orbit_mass, dt, sub_divs):
        self.stat_mass, self.orbit_mass, self.dt, self.sub_divs = stat_mass, orbit_mass, dt, sub_divs

    #a function that takes in position and velocity and returns an euler approximated final answer
    def new_position(self, Px, Py, Vx, Vy):

        #define a variable for time to reduce notation issues
        time = (FPS * self.dt) ** -1

        #define names for stat mass and orbit mass to keep code clean
        sm = self.stat_mass
        om = self.orbit_mass
        sub_divs = self.sub_divs

        #define a starting subdivision
        cur_sub_div = 1

        #make a while loop that repeats euler's method for the specified number of sub-intervals
        while cur_sub_div < sub_divs + 1:


            #creating new angle value based on sign of Px, Py, and inverse trig of these values
            theta = np.arctan2(Py, Px)

            #calculate new acceleration values based on previous position values
            a_mag = (G * sm * om) / (Px ** 2 + Py ** 2)

            #use angle to calculate acceleration components
            a_x = -a_mag * math.cos(theta)
            a_y = -a_mag * math.sin(theta)

            #creating new position values based on velocity values from a previous point
            Px = Px + Vx * time
            Py = Py + Vy * time

            #calculate new velocity values based on previous acceleration values
            Vx = Vx + a_x * time
            Vy = Vy + a_y * time

            #increment the current subdivision number
            cur_sub_div += 1

        #return a list with the position and velocity values so the game loop can hold them until the next new_position call
        print(Px, Py, Vx, Vy)
        return [Px, Py, Vx, Vy]

#define some initial values for the orbit simulation (mass, initial positions, and velocity)
#rename these to variables I will use in game loop
#if I give them an initial value and use these initial values in the game loop, but exactly the way I am trying to do it right now, I won't have to use as many object properties, and will make the code easier to understand

orbit_x = 100
orbit_y = 100
orbit_Vx = -3
orbit_Vy = 4
stat_mass = 5 * 10 ** 11
orbit_mass = 500

#need to set a value for how much time is represented in each frame, so I will choose ten seconds to enable easier testing
delta_time = 100

#variable for the number of subdivisions to use euler's method for on each frame
subdivisions = 500

#create an object of the calculations class with these initial values
calculator = Calculations(stat_mass, orbit_mass, delta_time, subdivisions)

#create a variable to hold the "running" state of the game loop
running = True

#create a clock to ensure a smooth FPS and manage time
clock = pygame.time.Clock()



#create the game loop, the code will automatically start the loop since it runs through the code linearly
while running:

    #adds a delay to keep frame rate at value of FPS
    clock.tick(FPS)

    #get the relative position values for the orbiting mass
    orbit_x = calculator.new_position(orbit_x, orbit_y, orbit_Vx, orbit_Vy)[0]
    orbit_y = calculator.new_position(orbit_x, orbit_y, orbit_Vx, orbit_Vy)[1]

    #check for user input, specifically whether the window is closed
    for event in pygame.event.get():
        #if the event is of type "QUIT" then the program closes
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #checking for arrow key input to change velocity

            if event.key == pygame.K_UP:
                orbit_Vy += 100 / FPS
            if event.key == pygame.K_DOWN:
                orbit_Vy -= 100 / FPS
            if event.key == pygame.K_RIGHT:
                orbit_Vx += 100 / FPS
            if event.key == pygame.K_LEFT:
                orbit_Vx -= 100 / FPS

            break


    # store the velocity values in the game loop so that we can use them from frame to frame
    orbit_Vx = calculator.new_position(orbit_x, orbit_y, orbit_Vx, orbit_Vy)[2]
    orbit_Vy = calculator.new_position(orbit_x, orbit_y, orbit_Vx, orbit_Vy)[3]

    # transform the relative coordinate system to the display coordinate system
    # +y vector for the pygame display is opposite of that in the typical cartesian setup, so I have to negate the y value
    # basically, the top left corner of the window is (0,0), and the bottom right is (Width, Height)
    scr_orbit_x = orbit_x + SCREEN_Width / 2
    scr_orbit_y = -orbit_y + SCREEN_Height / 2

    #fills the screen with black, redraws the rectangles at their new positions on the screen, then updates the display
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (scr_orbit_x, scr_orbit_y, 30, 30))

    pygame.draw.rect(screen, (0, 0, 255), (SCREEN_Width / 2, SCREEN_Height / 2, 30, 30))
    pygame.display.flip()



