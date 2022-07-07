# Python Imports
import time
import math

# Ev3Dev Imports
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create motors objects
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
tank = MoveTank(OUTPUT_A, OUTPUT_B)
steering = MoveSteering(OUTPUT_A, OUTPUT_B)

motorC = LargeMotor(OUTPUT_C) # Magnet

# Create objects
spkr = Sound()
btn = Button()
radio = Radio()

# Create sensors
color_left_sensor = ColorSensor(INPUT_1)
color_right_sensor = ColorSensor(INPUT_8)
gyro_sensor = GyroSensor(INPUT_3)
gps_sensor = GPSSensor(INPUT_4)
ultrasonic_front_sensor = UltrasonicSensor(INPUT_2)
ultrasonic_lateral_lower_sensor = UltrasonicSensor(INPUT_6)
ultrasonic_lateral_upper_sensor = UltrasonicSensor(INPUT_7)