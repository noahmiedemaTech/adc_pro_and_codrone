from codrone_edu.drone import *

drone = Drone()
drone.pair()

distance = input("How far would you like to test")

while True:
    velocity_x = drone.get_flow_velocity_x()
    velocity_y = drone.get_flow_velocity_y()
    print(f"\rX: {velocity_x}, Y: {velocity_y}", end="")