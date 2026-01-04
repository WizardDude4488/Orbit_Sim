import pygame
import random
import scipy
import math
import numpy as np
import array


from scipy.integrate import quad

#set up variable for screen size
SCREEN_Width = 670
SCREEN_Height = 450
SCREEN_SIZE = (SCREEN_Width, SCREEN_Height)

#set the mode of the display
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode(SCREEN_SIZE) #I think there's a problem with the screen object because I can't display anything on it
pygame.display.update()



#create an FPS variable
FPS = 60

#create a clock object to check the time/set frame rate
clock = pygame.time.Clock()

#main simulation loop
running = True

#define universal constant of gravitation, G
G = 6.67430 * (10 ** -11)

_current_time = 0


class Calculations:

    def _accel_gravity(self, G, mass_1, radius):
        # mass_1 is considered to be stationary for computational simplicity
        # defining object parameters
        self.G, self.mass_1, self.radius = G, mass_1, radius

        _accel_mag = (G * mass_1) / radius ** 2
        return _accel_mag

    def _velocity_new(self, _accel_mag, _accel_angle, _delta_time, mass_1, mass_2, _d_x, _d_y):
        # defining object parameters
        self._accel_mag, self._accel_vector, self._delta_time, self.mass_1, self.mass_2, self._d_x, self._d_y = _accel_mag, _accel_angle, _delta_time, mass_1, mass_2, _d_x, _d_y,

        # define a function for returning the force of gravity between the two objects
        def f(x):
            return G * mass_1 / (_d_x ** 2 + _d_y ** 2)

    def _position_new(self, G, steps, _delta_time, mass_1, mass_2, Vx, Vy, _pos_x, _pos_y):
        # defining object parameters
        self._delta_time, self.mass_1, self.mass_2, self.Vx, self.Vy, self.G, self._pos_x, self._pos_y, self.steps = steps, _delta_time, mass_1, mass_2, Vx, Vy, G, _pos_x, _pos_y

        intSteps = 0

        #make this method as simple as possible, don't try to put too much functionality in one method
        #make another class that uses this method in a while loop
        #that way, if there's a problem it will be easier to target a specific class and/or method to fix and improve, rather than getting lost in the unreadability of this mess

        #main functional problem is it seems the .sin and .cos functions aren't calculating negative values, so the acceleration is never negative in the simulation, which is a problem
        #maybe declare the posx and posy as the distance of the orbiting mass from the center
        #that way, we should get negative posx and posy values

        while intSteps < steps:
            #calculate the magnitude of the acceleration on the mass_2
            _accel_mag = (G * mass_1) / (_pos_x ** 2 + _pos_y ** 2)

            #get the angle of the orbiting object with the horizontal
            _theta = -1 * np.arcsin(_pos_y / (_pos_x ** 2 + _pos_y ** 2) ** 1/2)

            #get the x and y components of the mass_2's acceleration using the angle mass_2 creates with the position of mass_1 and the "horizontal"
            _accel_x = math.sin(_theta) * _accel_mag
            _accel_y = math.cos(_theta) * _accel_mag

            #calculate the new component velocities for the next position calculation
            _Vx_new = Vx + _accel_x * _delta_time

            _Vy_new = Vy + _accel_y * _delta_time

            #use the last position's component velocities for calculating the new x and y for this cycle
            _pos_x_new = _pos_x + Vx * _delta_time
            _pos_y_new = _pos_y + Vy * _delta_time

            intSteps = intSteps + 1

            if intSteps < steps:
                return [_Vx_new, _Vy_new, _pos_x_new, _pos_y_new]
            else:
                continue


        #give the new x and y values and the new velocities back
        return None




calculations = Calculations()

#create some initial values
Vx = 2
Vy = 0
_pos_x = 300
_pos_y = 100
mass_1_init = 5 * (10 ** 14)
mass_2_init = 5000

_orbit_x_init = _pos_x + SCREEN_Width / 2
_orbit_y_init = _pos_y + SCREEN_Height / 2


dt = clock.tick(FPS)
ds = dt/1000

while running:
    # call a command that makes sure the display only updates at 60 FPS
    #dt will give the time since last tick which can be used for integrating the acceleration components to find the velocity components
    #plan is to define all graphical objects as sprites, add them to one group, then in the events, rerun the calculations using the last frame data and then update and draw the group
    clock.tick(FPS)

    #define a change in time in seconds


    #get the pygame event checker
    for event in pygame.event.get():
        #if the event is of type "QUIT" then the program closes
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                pygame.draw.circle(screen, (255, 255, 255), (300, 225), 10)
        break

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255, 0, 0), (_pos_x, _pos_y, 30, 30))

    pygame.draw.rect(screen, (0, 0, 255), (SCREEN_Width / 2, SCREEN_Height / 2, 30, 30))
    pygame.display.flip()

    _values_ = calculations._position_new(G, 1000, ds, mass_1_init, mass_2_init, Vx, Vy, _pos_x, _pos_y)

    Vx = _values_[0]
    Vy = _values_[1]
    _pos_x = _values_[2]
    _pos_y = _values_[3]

    print(Vx, Vy, _pos_x, _pos_y)

    #while _current_time < 10*ds:

        #FYI each frame equals some number of time steps
        #get position for new time step
        #_values_ = calculations._position_new(G, 400, ds, mass_1_init, mass_2_init, Vx, Vy, _pos_x, _pos_y)

        #Vx = _values_[0]
        #Vy = _values_[1]
        #_pos_x = _values_[2]
        #_pos_y = _values_[3]

        #Janky way to simulate the physical extent of object 1
        #if _pos_x**2 + _pos_y**2 < 81:
            #running = False

        #set position tuple to new values
        #print(Vx, Vy, _pos_x, _pos_y)

        #_current_time = _current_time + ds


    #When the while loop is finished, update the display with the new values
    #figure out a way to simply move the orbiting object to the new position, delete the object from the display at the old position, and repeat the process






