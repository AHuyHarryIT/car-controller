#!/usr/bin/env python3
import pygame
import time
from gpio_driver import GPIODriver
from sequencer import set_state
from states import PINS

# Initialize GPIO driver
driver = GPIODriver(PINS)
driver.setup()

# Initialize pygame for joystick handling
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise RuntimeError("No Xbox controller detected! Connect one via USB or Bluetooth.")

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"🎮 Controller connected: {joystick.get_name()}")

# Mapping thresholds
AXIS_THRESHOLD = 0.4

def handle_input():
    """Reads controller input and runs corresponding movement actions."""
    pygame.event.pump()

    # Read axes (typically: 0 = left stick X, 1 = left stick Y)
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Button mapping
    a_button = joystick.get_button(0)  # A
    b_button = joystick.get_button(1)  # B
    x_button = joystick.get_button(2)  # X
    y_button = joystick.get_button(3)  # Y

    # Lock/Unlock
    if x_button:
        set_state(driver, "LOCK")
        time.sleep(0.2)
    elif y_button:
        set_state(driver, "UNLOCK")
        time.sleep(0.2)
    # Movement by analog stick
    elif y_axis < -AXIS_THRESHOLD:
        set_state(driver, "FORWARD")
    elif y_axis > AXIS_THRESHOLD:
        set_state(driver, "BACKWARD")
    elif x_axis < -AXIS_THRESHOLD:
        set_state(driver, "LEFT")
    elif x_axis > AXIS_THRESHOLD:
        set_state(driver, "RIGHT")
    elif a_button or b_button:
        # A or B pressed: immediate stop
        set_state(driver, "STOP")
    else:
        # No input: stop to prevent drift
        driver.stop()

def main():
    print("Use the left stick for movement.")
    print("X = Lock, Y = Unlock, A/B = Stop. Press Ctrl+C to exit.")
    try:
        while True:
            handle_input()
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        driver.cleanup()

if __name__ == "__main__":
    main()
