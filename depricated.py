from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

from codrone_edu.drone import *

import functions


def clamp_stick(value: float) -> int:
    """Clamp joystick values to the CoDrone EDU expected range (-100..100)."""
    try:
        value_int = int(value)
    except (TypeError, ValueError):
        value_int = 0
    return max(-100, min(100, value_int))


def record_joystick_csv(drone: Drone, csv_path: Path, hz: float = 20.0) -> None:
    if hz <= 0:
        raise ValueError("hz must be > 0")
    period_s = 1.0 / hz

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    start_t = time.monotonic()

    log_file = csv_path.open("w", newline="")
    writer = csv.writer(log_file)
    writer.writerow(["time", "left_joy_x", "left_joy_y", "right_joy_x", "right_joy_y"])
    log_file.flush()

    airborne = False
    try:
        # ! TODO add take off 
        drone.pair()
        #drone.takeoff()
        airborne = True

        while True:
            loop_start = time.monotonic()
            t = loop_start - start_t
            joystick = functions.handle_gamepad_input(drone)
            left_x = clamp_stick(joystick[0])
            left_y = clamp_stick(joystick[1])
            right_x = clamp_stick(joystick[2])
            right_y = clamp_stick(joystick[3])
            print(f"LX: {left_x}, LY: {left_y}, RX: {right_x}, RY: {right_y}")
            writer.writerow([t, left_x, left_y, right_x, right_y])
            log_file.flush()

            # Apply the combined control state in one call so flight stays responsive.
            drone.set_throttle(left_y)
            drone.set_yaw(left_x)
            drone.set_pitch(right_y)
            drone.set_roll(right_x)
            drone.move()

            if drone.l1_pressed():
                print("Stopping (L1 pressed)")
                break

            elapsed = time.monotonic() - loop_start
            time.sleep(max(0.0, period_s - elapsed))
    finally:
        log_file.close()
        if airborne:
            drone.land()
        drone.close()


def _default_log_name() -> str:
    return f"joystick_log_{time.strftime('%Y%m%d_%H%M%S')}.csv"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fly with the controller while logging joystick inputs to CSV."
    )
    parser.add_argument(
        "--out",
        default=_default_log_name(),
        help="Output CSV path (default: joystick_log_YYYYMMDD_HHMMSS.csv)",
    )
    parser.add_argument("--hz", type=float, default=20.0, help="Log/control rate (Hz)")
    args = parser.parse_args()

    out_path = Path(args.out)
    print(f"Logging joystick inputs to: {out_path.resolve()}")

    drone = Drone()
    record_joystick_csv(drone, out_path, hz=args.hz)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
