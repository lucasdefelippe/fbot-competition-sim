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
pen = Pen(INPUT_5)

# Create sensors
color_left_sensor = ColorSensor(INPUT_8)
color_right_sensor = ColorSensor(INPUT_1)
gyro_sensor = GyroSensor(INPUT_3)
gps_sensor = GPSSensor(INPUT_4)
ultrasonic_front_sensor = UltrasonicSensor(INPUT_2)
ultrasonic_lateral_lower_sensor = UltrasonicSensor(INPUT_6)
ultrasonic_lateral_upper_sensor = UltrasonicSensor(INPUT_7)
ultrasonic_right_upper_sensor = UltrasonicSensor(INPUT_9)



# Constant declaration
wheel_diameter = 5.6
centimetre_to_degress = (360 / (wheel_diameter * math.pi))

wheel_spacing = 19.7
wheel_robot_proportion = wheel_spacing / wheel_diameter

global_speed = SpeedDPS(50 * wheel_robot_proportion)
sensor_clocks = 0.1

line_follow_average_value = 50



# Modules
def line_follower(velocidade, back):
    if not back:
        color = color_right_sensor.reflected_light_intensity
    else:
        color = color_left_sensor.reflected_light_intensity
    error = (color - line_follow_average_value)
    steering_value = min(max(error, -100), error)

    # steering_value = steering_value * back

    steering.on(-steering_value if not back else steering_value, velocidade)

def line_follower_on_color(sensor, init_color):
    if sensor.color == init_color:
        steering.on(-30, global_speed)
    else:
        steering.on(30, global_speed)

def get_tube_distance():
    distance = ultrasonic_lateral_lower_sensor.distance_centimeters
    return distance

def get_tube_distance_right():
    distance = ultrasonic_right_upper_sensor.distance_centimeters
    return distance

def turn_on_degress(degress, wise):
    gyro_sensor.reset()
    original_angle = gyro_sensor.angle
    new_angle = original_angle
    while wise * new_angle <= degress:
        steering.on(wise * 100, global_speed)
        new_angle = gyro_sensor.angle
    steering.on(0, 0)

def get_robot_position():
    return (left_motor.position + right_motor.position) / 2

def reset_position():
    left_motor.position = 0
    right_motor.position = 0



# Code
tube_length = 25
max_tube_distance = 200
ultrasonic_error = 1
tube_orientation = 0 # 0 Horizontal; 1 Vertical.

while True:
    line_follower(global_speed, False)

    if get_tube_distance() < max_tube_distance:
        break

steering.on(0, 0)



tube_distance = get_tube_distance()
tube_distance_init_reading = tube_distance
reset_position()
tube_center_position = ((tube_distance * math.cos(80 * math.pi / 180)) + (tube_length / 2)) * centimetre_to_degress

while get_robot_position() < tube_center_position:
    
    current_tube_distance = get_tube_distance()
    if current_tube_distance < max_tube_distance:
        if not tube_distance - ultrasonic_error < current_tube_distance < tube_distance + ultrasonic_error:
            tube_orientation = 1
            break
        tube_distance = current_tube_distance

    line_follower(global_speed, False)



if tube_orientation == 0:
    turn_on_degress(90, -1)
    
    while ultrasonic_front_sensor.distance_centimeters > 5:
        steering.on(0, global_speed)



if tube_orientation == 1:
    turn_on_degress(180, 1)
    init_color = color_right_sensor.color
    while color_right_sensor.color == init_color:
        line_follower(global_speed, True)
    steering.on(0,0)

    turn_on_degress(90, 1)

    while True:
        line_follower_on_color(color_left_sensor, init_color)
    
        if get_tube_distance_right() < max_tube_distance:
            break



    tube_distance = get_tube_distance_right()
    tube_distance_init_reading = tube_distance
    reset_position()
    tube_center_position = ((tube_distance * math.cos(80 * math.pi / 180)) + (tube_length / 2)) * centimetre_to_degress



    while get_robot_position() < tube_center_position:
        line_follower_on_color(color_left_sensor, init_color)



    turn_on_degress(90, 1)
    while ultrasonic_front_sensor.distance_centimeters > 5:
        steering.on(0, global_speed)



steering.on(0, 0)




'''

steering.on(0,0)
time.sleep(1)
        
# Rotaciona
turn_180_degree_on_line()

time.sleep(1)
steering.on(0,0)

reset_position()

while get_robot_position() < tube_avarange_position:
    print("goal:",  tube_avarange_position, "position:", get_robot_position())
    line_follower(global_speed, True)
    
steering.on(0, 0)

'''



















