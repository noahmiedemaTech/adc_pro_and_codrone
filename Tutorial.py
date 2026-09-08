# import all codrone commands and tools.
from codrone_edu.drone import *
import time

# connect the drone and declare what the drone is for the library
drone = Drone()
drone.connect()

# python automatically defines variable type like int, string, or double
delay = 0.2

# First go through the try block
try:
    drone.takeoff()
    while True:
        # square
        # distance, unit ("cm" or 'in'), speed (0 to 1)
        drone.move_forward(10, 'in', 0.5)
        # delay in seconds
        time.sleep(delay)
        drone.move_left(10, 'in', 0.5)
        time.sleep(delay)
        drone.move_backward(10, 'in', 0.5)
        time.sleep(delay)
        drone.move_right(10, 'in', 0.5)
        # break the loop
        break

# if an error is caught always run this block
except Exception as e:
    print(e)

#then no matter the outcome of the try block, run this:
finally:
    drone.land()
    drone.close()