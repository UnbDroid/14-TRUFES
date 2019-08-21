from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from alinhamentoTempo import alinhaTempo
import time

# Definindo o nome das cores da matriz de cores
Preto = 0
Branco = 1

# Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

# Disponibilidade
Livre = True
Ocupada = False

tempo_centro_quadrado = 1  # Esse é o tempo que ele precisa para chegar ao centro do quadrado
dist_max = 2100  # Essa é a distância do primeiro ao último quadrado da linha
N = 804

def descerLateral(move_tank, motorEsq, motorDir, ultrassom, colorE, colorD):

	motorEsq.reset()
	motorDir.reset()
	distMotores = 0

	move_tank.on(SpeedPercent(40), SpeedPercent(40))
	while(N - distMotores > 0):
		distMotores = int((motorEsq.position + motorDir.position)/2)
		if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
			alinhaTempo(colorE, colorD, 40, move_tank, False)
	move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.04)
	move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 0.07)


def verificaLinha(move_tank, ultrassom, colorE, colorD, motorDir, linha):
	contador = 0
	distancia = 0
	ultravalue = 0
	flag = 0
	distMotor = motorDir.position
	while (contador < 10):
		distancia += ultrassom.value()
		contador += 1
	ultravalue = ultrassom.value()
	print(ultravalue)		
	distancia = int(distancia / 10)
	print("Distancia final: ", distancia)
	if (distancia < dist_max):  # Pode ser que o cubo esteja no último quadrado
		move_tank.on(SpeedPercent(50), SpeedPercent(50))
		while(distancia > 300 and flag != 2):  #Anda para melhor verificar
			print("ultraman:", distancia)
			if(flag):
				ultravalue = ultrassom.value()
				flag = 0
			else:
				flag = 1
			if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK and distancia > 320):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
				ultravalue = ultrassom.value()
			distancia = ultrassom.value()
			if(abs(distancia-ultravalue) > 200):
				flag = 2

		distancia = ultrassom.value()
		print(distancia)
		if(ultrassom.value() < 2100 and flag != 2):
			print(1)
			return True
		else:
			move_tank.on(SpeedPercent(-50), SpeedPercent(-50))
			while(motorDir.position - distMotor > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					alinhaTempo(colorE, colorD, 40, move_tank, True)

	print(0)
	if(linha != 7):
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.0)
	return False
