import csv
import numpy as np

# TODO Add Csv Data to be logged in inches
class Log:
    def __init__(self, drone, filename):
        self.drone = drone
        self.file = open(filename, "a", newline="")
        self.writer = csv.writer(self.file)

        self.writer.writerow([
            "front",
            "bottom",
        ])

    def log(self):
        front = self.drone.get_front_range("in")
        bottom = self.drone.get_bottom_range("in")


        self.writer.writerow([
            front,
            bottom
        ])

    def close(self):
        self.file.close()