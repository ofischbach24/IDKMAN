#!/usr/bin/env python3
import RPi.GPIO as GPIO
from evdev import InputDevice, ecodes
import threading
import socket
from motorlib import board, motor

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

# Function to continuously read and print gamepad events
def gamepad_event_loop():
    while True:
        events = get_gamepad()
        for event in events:
            print(f"Event: {event.ev_type}-{event.ev_code}, Value: {event.ev_value}")

# Start the gamepad event loop in a separate thread
gamepad_thread = threading.Thread(target=gamepad_event_loop)
gamepad_thread.start()

# Function to control motors
def motor_control(motor_pwm, joystick_value):
    motor_pwm.start(int(joystick_value * 100 * powerDrive))

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5555))
server_socket.listen(1)

print("Waiting for a client to connect...")
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# Main loop to continuously check gamepad input
try:
    while True:
        events = get_gamepad()
        for event in events:
            if event.ev_type == 'Absolute' and event.ev_code == 'ABS_Y':
                # Left stick vertical axis (up and down)
                left_stick_y = event.ev_value / 32767.0
                motor_control(left_tread_pwm, left_stick_y)

            elif event.ev_type == 'Absolute' and event.ev_code == 'ABS_RY':
                # Right stick vertical axis (up and down)
                right_stick_y = event.ev_value / 32767.0
                motor_control(right_tread_pwm, right_stick_y)

except KeyboardInterrupt:
    server_socket.close()
    GPIO.cleanup()
