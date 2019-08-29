from ev3dev2.motor import *
from time import sleep, clock

def filterultrassom(ultrassom):
	total = 0
	flag = 0

	valor1 = ultrassom.value()
	valor2 = valor1
	for i in range(0, 10):
		valor1 = ultrassom.value()
		timeIni = time.clock()
		while(valor1 == valor2 and flag == 0 and (time.clock() - timeIni) < 0.1):
			valor1 = ultrassom.value()
			if(valor1 < 80):
				for i in range (0, 3):
					valor1 += ultrassom.value()
				if(valor1 < 320):
					break
				else:
					valor1 = int(valor1/3)
		flag = 1
		total += valor1

	return int(total/10)

def drift(super, move_tank, move_steering):
	#Se super for True, o robô vai dar drift de ré.
	#Se não, ele faz a volta na lavanderia
	if(super):
		# Porcentagem de graus baseado na velocidade da roda pivô
		# Ex: Quando vale 25, a roda direita girará a metade da velocidade da roda esquera, e contrario é valido para 75.
		# < 0 == Esquerda como pivô
		# > 0 == Direita como pivô
		# == 0 Continua reto
		move_steering.on_for_rotations(25, SpeedPercent(-50), 4.6)
		move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40), 0.05)
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 0.6)
		
	else:
		# Contorna Cubo
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 2.252) # Anda um quadrado
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05) # 90º direita
		move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 2.252) # anda um quadrado
		move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 2.05) # 180º esquerda
