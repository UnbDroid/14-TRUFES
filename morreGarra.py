from ev3dev2.motor import *
from ev3dev2.sensor.lego import *


def main():
	move_garra = MoveTank(OUTPUT_A, OUTPUT_B, motor_class=MediumMotor)
	move_garra.on_for_rotations(SpeedPercent(-10),SpeedPercent(10), 0.2)
	move_garra.on(SpeedPercent(10),SpeedPercent(-10))
	move_garra.wait_until_not_moving()

main()