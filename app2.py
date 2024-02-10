#!/usr/bin/env python3
from colorama import Fore
from motorlib import board, motor
import RPi.GPIO as GPIO
from evdev import InputDevice, ecodes
from inputs import get_gamepad

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup Boards
pi = board('pi', type="pi")

# Setup Motors
RightTread = motor(pi, pins=[1, 11])
LeftTread = motor(pi, pins=[2, 12])

# Setup Power Variables
powerDrive = 1

# Define deadzone threshold
DEADZONE_THRESHOLD = 0.2

def apply_deadzone(value, threshold):
    return 0 if abs(value) < threshold else value

def Shutdown(message):
    if message:
        # Sets all motors to 0
        RightTread.start(0)
        LeftTread.start(0)

        print(Fore.RED + 'Shutdown' + Fore.RESET)

# Path to the event file for the gamepad, adjust as needed
gamepad_path = "/dev/input/eventX"  # Replace eventX with the correct event file
gamepad = InputDevice(gamepad_path)

try:
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_Y:
                joystick1_value = event.value / 32767.0
                joystick1_value = apply_deadzone(joystick1_value, DEADZONE_THRESHOLD)
                LeftTread.start(int(joystick1_value * 100 * powerDrive))

            elif event.code == ecodes.ABS_RX:
                joystick2_value = event.value / 32767.0
                joystick2_value = apply_deadzone(joystick2_value, DEADZONE_THRESHOLD)
                RightTread.start(int(joystick2_value * 100 * powerDrive))

        elif event.type == ecodes.EV_KEY and event.code == ecodes.BTN_START:
            shutdown_value = event.value
            Shutdown(shutdown_value)

except KeyboardInterrupt:
    GPIO.cleanup()
