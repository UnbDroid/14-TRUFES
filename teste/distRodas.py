from ev3dev2.motor import *
from ev3dev2.sensor.lego import *

move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
motorEsq = LargeMotor(OUTPUT_C)
motorDir = LargeMotor(OUTPUT_D)
Velocidade = 20

def main():
	motorEsq.reset()
	motorDir.reset()

	a = motorEsq.position
	b = motorDir.position
	move_tank.on_for_rotations(SpeedPercent(Velocidade), SpeedPercent(Velocidade), 1)
	a = motorEsq.position
	b = motorDir.position
	print('Esquerda 1:', a, 'Direita 1:', b, )
	move_tank.on_for_rotations(SpeedPercent(Velocidade), SpeedPercent(Velocidade), 2)
	a = motorEsq.position
	b = motorDir.position	
	print('Esquerda 2:', a, 'Direita 2:', b, )
	a = motorEsq.position
	b = motorDir.position
	move_tank.on_for_rotations(SpeedPercent(Velocidade), SpeedPercent(Velocidade), 3)
	a = motorEsq.position
	b = motorDir.position
	print('Esquerda 3:', a, 'Direita 3:', b, )
	motorEsq.reset()
	motorDir.reset()
	move_tank.on_for_rotations(SpeedPercent(Velocidade), SpeedPercent(Velocidade), 3)
	a = motorEsq.position
	b = motorDir.position
	print('Esquerda 4:', a, 'Direita 4:', b, )
	motorEsq.reset()
	motorDir.reset()
	move_tank.on_for_rotations(SpeedPercent(Velocidade), SpeedPercent(Velocidade), 6)
	a = motorEsq.position
	b = motorDir.position
	print('Esquerda 5:', a, 'Direita 5:', b, )	
	#::TESTES

main()