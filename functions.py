import Constants
import SensorFilter


def handle_gamepad_input(drone):
    lx = drone.get_left_joystick_x() / 10
    ly = drone.get_left_joystick_y() / 10
    rx = drone.get_right_joystick_x() / 10
    ry = drone.get_right_joystick_y() / 10
    lt = 5 * 2 
    
    return lx, ly, rx, ry, lt



# drone, target box (1 or 2), do you want to use coordinate
def enter_holes(drone, target_box: int, coordinate: bool):
    #bottom_range = SensorFilter.Filter(lambda: drone.get_bottom_range("in"), 5)
    #front_range = SensorFilter.Filter(lambda: drone.get_front_range("in"), 5)
    if target_box == 1:
        x_pos = Constants.x_pos_box_1
        y_pos = Constants.y_pos_box_1
        z_pos = Constants.z_pos_box_1
        heading_box = Constants.heading_box_1
    elif target_box == 2:
        x_pos = Constants.x_pos_box_2
        y_pos = Constants.y_pos_box_2
        z_pos = Constants.z_pos_box_2
        heading_box = Constants.heading_box_2
    else:
        raise ValueError("Target box must be 1 or 2 for function detect_holes")

    if coordinate:
        drone.send_absolute_position(x_pos, y_pos, z_pos, 1, heading_box, 0.5)
        detect_holes(drone)
        drone.move_forward(Constants.box_forward_distance_coordinate)
    if not coordinate:
        # TODO non coordinate hole scanning
        raise ValueError("Non coordinate hole scanning unfinished")


def detect_holes(drone):
    front_range = SensorFilter.Filter(lambda: drone.get_front_range("in"), 5)
    while front_range.update() >= 20:
        drone.set_roll(3)
        drone.move()
    drone.set_roll(0)
    drone.move(0.1)


def inches_to_cm(inches):
    return inches * 2.54


def cm_to_inches(cm):
    return cm / 2.54


def distance_2d(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def meter_to_inch(meter):
    return meter / 39.3701
