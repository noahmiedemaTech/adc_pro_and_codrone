from codrone_edu.drone import *

import CSV_Log
import SensorFilter
import functions

drone = Drone()
drone.pair()


try:

except Exception as e:
    print(e)

finally:
    drone.land()
