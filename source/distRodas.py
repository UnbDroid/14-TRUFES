from ev3dev2.motor import *
from ev3dev2.sensor.lego import *


def drift(super):
#Se super for True, o robô vai dar drift de ré.
#Se não, ele faz a volta na lavanderia
	move_steering = MoveSteering(OUTPUT_C, OUTPUT_D)
	move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
	if(super):
		move_steering.on_for_rotations(-20, SpeedPercent(-50), 4.2)
	else:
		move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2.252)
		move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.05)
		move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2.252)
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)

drift(True)