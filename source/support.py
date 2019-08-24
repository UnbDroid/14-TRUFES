from ev3dev2.motor import *

def filterultrassom(ultrassom):
	valor = 0
	for i in range(0, 5):
		valor += ultrassom.value()
	print("VAL:", valor/5)
	return int(valor/5)

def drift(super, move_tank, move_steering):
	#Se super for True, o robô vai dar drift de ré.
	#Se não, ele faz a volta na lavanderia
	if(super):
		move_steering.on_for_rotations(22, SpeedPercent(-50), 4.45)
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 0.7)
	else:
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 2.252)
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 2.252)
		move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 2.05)
