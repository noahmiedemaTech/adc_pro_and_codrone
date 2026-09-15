class Filter:
    def __init__(self, sensor, range_of_data):
        self.sensor = sensor
        self.readings = []
        self.total = 0
        self.average_data = 0
        self.sorted_data = []
        self.range_of_data = range_of_data

    def update(self):
        # Call sensor data
        self.readings = []

        for i in range(self.range_of_data):
            reading = self.sensor()
            self.readings.append(reading)

        # Remove spikes
        self.sorted_data = sorted(self.readings)
        self.sorted_data.pop(0)
        self.sorted_data.pop(-1)

        average = self.average()
        return average

    def average(self):
        # Smooth data
        self.total = sum(self.sorted_data)
        self.average_data = self.total / len(self.sorted_data)
        return self.average_data