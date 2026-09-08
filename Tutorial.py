# import all codrone commands and tools.
from codrone_edu.drone import *
import time

#connect the drone and declare what the drone is for the library
drone = Drone()
drone.connect()

drone.takeoff()

while True:
    pass