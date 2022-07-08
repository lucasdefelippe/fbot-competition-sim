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
    steering.on(-steering_value if not back else steering_value, velocidade)


def tube_detection():
    distance = ultrasonic_lateral_lower_sensor.distance_centimeters
    if distance >= 200:
        return False
    else:
        return True

def turn_180_degree_on_line():
    start_time = time.time()
    while color_left_sensor.color != 6:
        steering.on(100, global_speed)
    time.sleep(0.5)
    steering.on(0, 0)
    end_time = time.time()
    return end_time - start_time



# Code
follow_line = True
tube_detection_state = False
steering.on(0, global_speed)

tubo_mode_timer_start = True

while True:
    # Continua seguindo a linha até mandarem parar
    if follow_line:
        line_follower(global_speed, False)
    else:
        steering.on(0, 0)


    # Caso detecte um tubo e set o tempo aonde ele foi encontrado
    has_tube = tube_detection()
    if has_tube and not tube_detection_state and follow_line:
        tube_init_time = time.time()
        tube_detection_state = True
    # Quando o tubo detectado a cima "acaba", set o tempo aonde ele acabou
    if not has_tube and tube_detection_state and follow_line:
        tube_end_time = time.time()
        tube_detection_state = False
        follow_line = False
        
        # Calcula o quanto o robo tem que voltar
        tube_avarange_time = (tube_end_time - tube_init_time) / 2
        
        print(tube_avarange_time)


    # Modo ir até o tubo
    if not follow_line:
        if tubo_mode_timer_start:
            back_path_init_time = time.time()
            print(back_path_init_time)
            tubo_mode_timer_start = False

        turn_interval = turn_180_degree_on_line()

        while time.time() - back_path_init_time < tube_avarange_time + turn_interval:
            line_follower(global_speed, True)
            print(time.time())
        steering.on(0, 0)



















