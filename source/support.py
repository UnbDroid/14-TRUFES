from ev3dev2.motor import *

def filterultrassom(ultrassom):
	valor = 0
	for i in range(0, 10):
		valor += ultrassom.value()
	return int(valor/10)

def drift(super, move_tank, move_steering):
	#Se super for True, o robô vai dar drift de ré.
	#Se não, ele faz a volta na lavanderia
	if(super):
		# Porcentagem de graus baseado na velocidade da roda pivô
		# Ex: Quando vale 25, a roda direita girará a metade da velocidade da roda esquera, e contrario é valido para 75.
		# < 0 == Esquerda como pivô
		# > 0 == Direita como pivô
		# == 0 Continua reto
		move_steering.on_for_rotations(25, SpeedPercent(-50), 4.7)
		move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40), 0.12)
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 0.7)
	else:
		# Contorna Cubo
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 2.252) # Anda um quadrado
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05) # 90º direita
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 2.252) # anda um quadrado
		move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 2.05) # 180º esquerda
