import csv
import enum
import time

from codrone_edu.drone import Drone

drone = Drone()


class State(enum.Enum):
    Start = 0
    Colorpad = 1
    Reading = 2
    Break = 3


state = State.Start


def handle_break(info):
    print(f"Break encountered. Handling break with info: {info}")
    if info == "Colorpad":
        print("Handling Colorpad break.")
        drone.land()
        drone.get_color_data()
        print(f"Color data: {drone.get_color_data()}")


def main():
    try:
        drone.pair()
        flying = False
        # ! Add drone takeoff command here
        drone.takeoff()
        
        flying = True
        state = State.Reading
        
        with open("joystick_log.csv", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if state == State.Reading:
                    if row["left_stick_x"] == "break":
                        state = State.Break
                        print(f"Break encountered with info: {row['break_info']}")
                    else:
                        drone.set_throttle(int(float(row["left_stick_y"])))
                        drone.set_roll(int(float(row["right_stick_x"])))
                        drone.set_pitch(int(float(row["right_stick_y"])))
                        drone.set_yaw(int(float(row["left_stick_x"])))
                        drone.move()
                        time.sleep(0.1)
                if state == State.Break:
                    handle_break(row["break_info"])
                    state = State.Reading
                    print("Resuming reading state.")

    except Exception as e:  # noqa: BLE001
        print(f"Failed to connect to the drone: {e}")

    finally:
        if flying:
            drone.land()


if __name__ == "__main__":
    main()
