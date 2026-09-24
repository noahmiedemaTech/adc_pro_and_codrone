from codrone_edu.drone import *

from constructs import functions
from constructs import Constants

import time

drone = Drone()
drone.pair()

try:
    drone.takeoff()
    drone.send_absolute_position(functions.meter_to_inch(1), functions.meter_to_inch(120), functions.meter_to_inch(17), 0.8, 0, 0)
    #drone.turn_left()
    #print("Location reached")
    #time.sleep(1)
    #print("Sleep Finished")
    #drone.send_absolute_position(functions.meter_to_inch(-48), functions.meter_to_inch(120), functions.meter_to_inch(31), 0.8, 0, 0)

    print("Location reached")
    #time.sleep(1)
    print("Sleep Finished")


except Exception as e:
    print(e)

finally:
    drone.land()
