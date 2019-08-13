from ev3dev2.motor import *
from ev3dev2.sensor.lego import *

move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
motorEsq = LargeMotor(OUTPUT_C)
motorDir = LargeMotor(OUTPUT_D)


def main():
	motorEsq.reset()
	motorDir.reset()

	a = motorEsq.position
	b = motorDir.position
	move_tank.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1)
	print('Esquerda 1:', a, 'Direita 1:', b, )
	move_tank.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 2)
	print('Esquerda 2:', a, 'Direita 2:', b, )
	a = motorEsq.position
	b = motorDir.position
	move_tank.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 3)
	print('Esquerda 3:', a, 'Direita 3:', b, )

	#::TESTES