from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

from codrone_edu.drone import *

import functions

data_multiplier_for_flyer = 6.0
data_multiplier_for_logger = 3


def clamp_stick(value: float) -> int:
    """Clamp joystick values to the CoDrone EDU expected range (-100..100)."""
    try:
        value_int = int(value)
    except (TypeError, ValueError):
        value_int = 0
    return max(-100, min(100, value_int))


def record_joystick_csv(drone: Drone, out_path: Path, hz: float) -> None:
    """Record joystick inputs to a CSV file at the specified rate (Hz)."""
    if hz <= 0:
        raise ValueError("Hz must be a positive number.")
    period_s = 1.0 / hz
    start_t = time.monotonic()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    log_file = out_path.open(mode="w", newline="")
    writer = csv.writer(log_file)
    writer.writerow(
        ["timestamp", "left_stick_x", "left_stick_y", "right_stick_x", "right_stick_y"]
    )
    flying = False
    try:
        drone.pair()
        # ! TODO ADD TAKEOFF
        drone.takeoff()
        flying = True
        while True:
            timestamp = time.monotonic()
            t = timestamp - start_t
            joystick = functions.handle_gamepad_input(drone)
            left_stick_x = clamp_stick(joystick[0])
            left_stick_y = clamp_stick(joystick[1])
            right_stick_x = clamp_stick(joystick[2])
            right_stick_y = clamp_stick(joystick[3])
            print(
                "Left stick:",
                left_stick_x,
                left_stick_y,
                "Right stick:",
                right_stick_x,
                right_stick_y,
            )
            writer.writerow(
                [
                    timestamp,
                    left_stick_x * data_multiplier_for_logger,
                    left_stick_y * data_multiplier_for_logger,
                    right_stick_x * data_multiplier_for_logger,
                    right_stick_y * data_multiplier_for_logger,
                ]
            )
            log_file.flush()

            drone.set_throttle(left_stick_y * data_multiplier_for_flyer)
            drone.set_yaw(left_stick_x * data_multiplier_for_flyer)
            drone.set_pitch(right_stick_y * data_multiplier_for_flyer)
            drone.set_roll(right_stick_x * data_multiplier_for_flyer)
            drone.move()

            if drone.l1_pressed():
                print("Stopping (L1 pressed)")
                break

            if drone.l2_pressed():
                drone.hover()
                print("Breaking point (L2 pressed)")
                z = drone.get_pos_z()
                print(f"Current altitude (Z): {z}")
                reason = input("Enter breaking reason: ")
                writer.writerow([timestamp, "", "", "", "", z, reason, "breakj"])
                log_file.flush()

            elapsed = time.monotonic() - timestamp
            time.sleep(max(0.0, period_s - elapsed))
    finally:
        log_file.close()
        if flying:
            drone.land()
        drone.disconnect()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fly with the controller while logging joystick inputs to CSV."
    )
    parser.add_argument(
        "--bockbock",
        default="joystick_log.csv",
        help="Output CSV path (default: joystick_log.csv)",
    )
    parser.add_argument(
        "--chicken", type=float, default=20.0, help="Log/control rate (Hz)"
    )
    args = parser.parse_args()

    out_path = Path(args.bockbock)
    print(f"Logging joystick inputs to: {out_path.resolve()}")

    drone = Drone()
    record_joystick_csv(drone, out_path, hz=args.chicken)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
