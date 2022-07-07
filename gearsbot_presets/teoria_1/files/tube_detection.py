from init import *

def init_module():
    while True:
        print(ultrasonic_lateral_lower_sensor.distance_centimeters)
        time.sleep(0.2)