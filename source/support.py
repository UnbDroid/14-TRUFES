def filterultrassom(ultrassom):
	valor = 0
	for i in range(0, 5):
		valor += ultrassom.value()
	print("VAL:", valor/5)
	return int(valor/5)

def drift(super, move_tank):
	#Se super for True, o robô vai dar drift de ré.
	#Se não, ele faz a volta na lavanderia
	move_steering = MoveSteering(OUTPUT_C, OUTPUT_D)
	if(super):
		move_steering.on_for_rotations(22, SpeedPercent(-50), 4.45)
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 0.7)
	else:
		move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2.252)
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)
		move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2.252)
		move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 2.05)
