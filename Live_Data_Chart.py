import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from codrone_edu.drone import *

import SensorFilter

drone = Drone()
drone.pair()
front_range = SensorFilter.Filter(lambda: drone.get_front_range('in'), 6)


data = []

fig, ax = plt.subplots()

def update(frame):
    reading = front_range.update()
    #reading = drone.get_front_range('in')
    data.append(reading)

    # Keep the graph from growing forever
    if len(data) > 100:
        data.pop(0)

    ax.clear()
    ax.plot(data)

    ax.set_title("Front Range")
    ax.set_xlabel("Reading")
    ax.set_ylabel("Distance (in)")

ani = FuncAnimation(
    fig,
    update,
    interval=100,
    cache_frame_data=False
)

plt.show()