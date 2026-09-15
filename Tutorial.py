from codrone_edu.drone import *
import time

# ──────────────────────────────────────────────
# CONNECTING THE DRONE
# ──────────────────────────────────────────────
drone = Drone()
drone.connect()

# ──────────────────────────────────────────────
# DATA TYPES IN PYTHON
# ──────────────────────────────────────────────

# INT (integer) — a whole number with no decimal point.
# Used below for DISTANCE: "fly 10 inches forward."
# You can do math with ints: 10 + 5, 15 * 2
# Python does it automatically
# distance = 5 + 5 (result is 10, an int)
distance = 10          # this is an int

# FLOAT (double) — a number WITH a decimal point.
# Used below for SPEED (0 to 1) and DELAY in seconds.
# 0.5 means "half speed," 0.2 means "wait 0.2 seconds."
# You can mix ints and floats: 10 * 0.5 = 5.0 (result is a float)
speed = 0.5            # this is a float
delay = 0.2            # this is a float

# STRING — text wrapped in quotes (single ' or double ").
# Used below for the UNIT of measurement: 'in' or 'cm'.
# The codrone python library needs the unit as a string to interpret "10" as 10 inches
unit = 'in'            # this is a string

# BOOLEAN — only two possible values: True or False.
# Used below in "while True" — the loop runs forever because the condition is always True.
condition = True       # this is a boolean

# ──────────────────────────────────────────────
# FLY A SQUARE
# ──────────────────────────────────────────────

try:
    drone.takeoff()

# A "while loop" repeats a block of code as long as
# a condition is True. Each full pass through the block
# is called one "iteration."

# while True:
#   ── True is a BOOLEAN (always the value True)
#   ── Since it never becomes False, the loop NEVER
#      stops on its own. This is called an "infinite loop."
#   ── The ONLY ways out are:
#        1. A `break` statement inside the loop
#        2. An error/exception (caught by try/except)
#        3. Ctrl+C in the terminal (manual stop)
    while True:        
        # move_forward(distance, unit, speed)
        #   distance → int (how far)
        #   unit     → string ('in' or 'cm')
        #   speed    → float (0.0 to 1.0)
        drone.move_forward(distance, unit, speed)
        time.sleep(delay)          # delay is a float (seconds)

        drone.move_left(distance, unit, speed)
        time.sleep(delay)

        drone.move_backward(distance, unit, speed)
        time.sleep(delay)

        drone.move_right(distance, unit, speed)
        time.sleep(delay)

        break        # exit the while loop after one square

# If ANY error occurs in the try block (crash, disconnect, typo),
# Python jumps here instead of freezing:
except Exception as e:
    print(e)        # e is a string containing the error message

# This ALWAYS runs, whether the try succeeded or failed.
# Guarantees the drone lands and the connection closes:
finally:
    drone.land()
    drone.close()