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



# Constant declaration
wheel_diameter = 5.6
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


def tube_detection():
    distance = ultrasonic_lateral_lower_sensor.distance_centimeters
    if distance >= 200:
        return False
    else:
        return True

def turn_180_degree_on_line():
    gyro_sensor.reset()
    original_angle = gyro_sensor.angle
    new_angle = original_angle
    while new_angle <= 180:
        steering.on(100, global_speed)
        new_angle = gyro_sensor.angle
    steering.on(0, 0)

def get_robot_position():
    return (left_motor.position + right_motor.position) / 2

def reset_position():
    left_motor.position = 0
    right_motor.position = 0




# Code
tube_init_position = None
tube_end_position = None
tube_avarange_position = 0

while True:
    # Continua seguindo a linha até mandarem parar
    line_follower(global_speed, False)

    # Caso detecte um tubo e set o tempo aonde ele foi encontrado
    has_tube = tube_detection()
    
    if has_tube and not tube_init_position:
        tube_init_position = get_robot_position()

    # Quando o tubo detectado a cima "acaba", set o tempo aonde ele acabou
    if not has_tube and tube_init_position != None:
        tube_end_position = get_robot_position()
        tube_avarange_position = (tube_end_position - tube_init_position)
        break
    
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




















