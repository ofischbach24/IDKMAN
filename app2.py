#!/usr/bin/env python3
import subprocess  # Added missing import
from colorama import Fore
import RPi.GPIO as GPIO
from motorlib import board, motor
from evdev import InputDevice, ecodes
from inputs import get_gamepad
import threading

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Function to get information about connected game controllers using xinput
def get_gamepad_info():
    try:
        result = subprocess.run(['xinput', 'list'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running xinput: {e}")
        return None

# Setup Motors
LEFT_TREAD_PINS = [2, 12]
RIGHT_TREAD_PINS = [1, 11]

GPIO.setup(LEFT_TREAD_PINS[0], GPIO.OUT)
GPIO.setup(LEFT_TREAD_PINS[1], GPIO.OUT)
GPIO.setup(RIGHT_TREAD_PINS[0], GPIO.OUT)
GPIO.setup(RIGHT_TREAD_PINS[1], GPIO.OUT)

left_tread_pwm = GPIO.PWM(LEFT_TREAD_PINS[0], 100)
right_tread_pwm = GPIO.PWM(RIGHT_TREAD_PINS[0], 100)

# Setup Power Variables
powerDrive = 1

# Example usage of get_gamepad_info
gamepad_info = get_gamepad_info()
if gamepad_info:
    print("Gamepad Information:")
    print(gamepad_info)

# Function to continuously read and print gamepad events
def gamepad_event_loop():
    while True:
        events = get_gamepad()
        for event in events:
            print(f"Event: {event.ev_type}-{event.ev_code}, Value: {event.ev_value}")

# Start the gamepad event loop in a separate thread
gamepad_thread = threading.Thread(target=gamepad_event_loop)
gamepad_thread.start()

# Define deadzone threshold
DEADZONE_THRESHOLD = 0.2

def apply_deadzone(value, threshold):
    return 0 if abs(value) < threshold else value

def motor_control(motor_pwm, joystick_value):
    motor_pwm.start(int(joystick_value * 100 * powerDrive))

def shutdown():
    stopall()
    GPIO.cleanup()
    print(Fore.RED + 'Shutdown' + Fore.RESET)

# Main loop to continuously check gamepad input
if __name__ == '__main__':
    print(Fore.RED + 'Server started' + Fore.RESET)
    try:
        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type == 'Absolute' and event.ev_code == 'ABS_Y':
                    # Left stick vertical axis (up and down)
                    left_stick_y = event.ev_value / 32767.0
                    left_stick_y = apply_deadzone(left_stick_y, DEADZONE_THRESHOLD)
                    motor_control(left_tread_pwm, left_stick_y)

                elif event.ev_type == 'Absolute' and event.ev_code == 'ABS_RY':
                    # Right stick vertical axis (up and down)
                    right_stick_y = event.ev_value / 32767.0
                    right_stick_y = apply_deadzone(right_stick_y, DEADZONE_THRESHOLD)
                    motor_control(right_tread_pwm, right_stick_y)

                elif event.ev_type == 'Key' and event.ev_code == 'BTN_START' and event.ev_value == 1:
                    shutdown()

    except KeyboardInterrupt:
        shutdown()

# Path to the event file for the gamepad, adjust as needed
# Replace "eventX" with the correct event file path for your gamepad
gamepad_path = "/dev/input/eventX"
gamepad = InputDevice(gamepad_path)

try:
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_Y:
                joystick1_value = event.value / 32767.0
                joystick1_value = apply_deadzone(joystick1_value, DEADZONE_THRESHOLD)
                motor_control(left_tread_pwm, joystick1_value)

            elif event.code == ecodes.ABS_RX:
                joystick2_value = event.value / 32767.0
                joystick2_value = apply_deadzone(joystick2_value, DEADZONE_THRESHOLD)
                motor_control(right_tread_pwm, joystick2_value)

        elif event.type == ecodes.EV_KEY and event.code == ecodes.BTN_MODE and event.ev_value == 1:
            shutdown_value = event.value
            shutdown()

except KeyboardInterrupt:
    GPIO.cleanup()
