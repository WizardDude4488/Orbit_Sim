import pygame
import random
import scipy
import math
import numpy as np
import array


from scipy.integrate import quad

#set up variable for screen size
SCREEN_Width = 1280
SCREEN_Height = 720
SCREEN_SIZE = (SCREEN_Width, SCREEN_Height)

#set the mode of the display
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.update()



#create an FPS variable
FPS = 120

#create a clock object to check the time/set frame rate
clock = pygame.time.Clock()

#main simulation loop
running = True

#define universal constant of gravitation, G
global G
G = 6.67430 * (10 ** -11)

_current_time = 0


class Calculations:

    def _position_new(self, G, _delta_time, mass_1, mass_2, Vx, Vy, _pos_x, _pos_y):
        # defining object parameters
        self._delta_time, self.mass_1, self.mass_2, self.Vx, self.Vy, self.G, self.in_pos_x, self.in_pos_y, = _delta_time, mass_1, mass_2, Vx, Vy, G, _pos_x, _pos_y

        #make this method as simple as possible, don't try to put too much functionality in one method
        #make another class that class this method in a while loop
        #that way, if there's a problem it will be easier to target a specific class and/or method to fix and improve, rather than getting lost in the unreadability of this mess

        #main functional problem is it seems the .sin and .cos functions aren't calculating negative values, so the acceleration is never negative in the simulation, which is a problem
        #maybe declare the posx and posy as the distance of the orbiting mass from the center
        #that way, we should get negative posx and posy values


        #calculate the magnitude of the acceleration on the mass_2
        _accel_mag = (G * mass_1) / (_pos_x ** 2 + _pos_y ** 2)

        #get the angle of the orbiting object with the horizontal
        if _pos_x < 0:
            global _theta
            _theta = np.arcsin(_pos_y / math.sqrt(_pos_x ** 2 + _pos_y ** 2))
        else:
            _theta = np.arcsin(_pos_y / math.sqrt(_pos_x ** 2 + _pos_y ** 2))

        #get the x and y components of the mass_2's acceleration using the angle mass_2 creates with the position of mass_1 and the "horizontal"
        _accel_x = math.sin(_theta) * _accel_mag
        _accel_y = math.cos(_theta) * _accel_mag

        #calculate the new component velocities for the next position calculation
        _Vx_new = Vx + _accel_x * _delta_time

        _Vy_new = Vy + _accel_y * _delta_time

        #use the last position's component velocities for calculating the new x and y for this cycle
        _pos_x_new = _pos_x + Vx * _delta_time
        _pos_y_new = _pos_y + Vy * _delta_time

        return [_Vx_new, _Vy_new, _pos_x_new, _pos_y_new, _theta]


        #give the new x and y values and the new velocities back



calculations = Calculations()

class looperClass:
    def loop(self, Vx, Vy, _pos_x, _pos_y, final_subdivisions):
        self.Vx, self.Vy, self._pos_x, self._pos_y, self.final_subdivisions = Vx, Vy, _pos_x, _pos_y, final_subdivisions

        current_subdivision = 0 #start at zero

        dt = 1 / (final_subdivisions * FPS) #basically, the number of seconds is equal to 1 over the number of subdivisions times the frames per second we want to run at

        while current_subdivision < final_subdivisions:
            _values_ = calculations._position_new(G, dt, mass_1_init, mass_2_init, Vx, Vy, _pos_x, _pos_y) #run a _position_new calculation each cycle

           #getting values for next subdivision
            Vx = _values_[0]
            Vy = _values_[1]
            _pos_x = _values_[2]
            _pos_y = _values_[3]

            current_subdivision = current_subdivision + 1 #increment the subdivision number

        return np.array([_pos_x, _pos_y]) #when the frame is done being calculated, return the information we need to render the next frame

looper = looperClass()


# create some initial values
Vx = 10
Vy = 0
sc_pos_x = 300
sc_pos_y = 400
mass_1_init = 5 * (10 ** 14)
mass_2_init = 5000
_pos_x = sc_pos_x - SCREEN_Width / 2
_pos_y = sc_pos_y - SCREEN_Height / 2


dt = clock.tick(FPS)
ds = dt/1000
final_subd = 100

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
        break

    calculation_values = np.array([Vx, Vy, _pos_x, _pos_y])

    _frame_data = looper.loop(calculation_values[0], calculation_values[1], calculation_values[2], calculation_values[3], final_subd)

    sc_pos_x = looper.loop[0] + SCREEN_Width / 2
    sc_pos_y = looper.loop[1] + SCREEN_Height / 2

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255, 0, 0), (sc_pos_x, sc_pos_y, 30, 30))

    pygame.draw.rect(screen, (0, 0, 255), (SCREEN_Width / 2, SCREEN_Height / 2, 30, 30))
    pygame.display.flip()



    print(Vx, Vy, _pos_x, _pos_y, theta)






