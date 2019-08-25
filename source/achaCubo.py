from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from alinhamentoTempo import alinhaTempo
from support import filterultrassom
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
dist_max = 2100  # Essa é a distância do primeiro ao último quadrado visivel da linha
N = 804

def descerLateral(move_tank, motorEsq, motorDir, ultrassom, colorE, colorD):

	motorEsq.reset()
	motorDir.reset()
	distMotores = 0
	
	# Desce a lateral com base em N, que é a distância de um quadrado
	move_tank.on(SpeedPercent(40), SpeedPercent(40))
	while(N - distMotores > 0):
		distMotores = int((motorEsq.position + motorDir.position)/2)
		# Faz o alinhamento
		if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
			alinhaTempo(colorE, colorD, 40, move_tank, False)
	move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.04) # Vira 90º à esquerda
	move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 0.07) # Ajuste do erro de ré


def verificaLinha(move_tank, ultrassom, colorE, colorD, motorDir, linha):
	distancia = 0
	ultravalue = 0
	flag = 0
	distMotor = motorDir.position
	distancia = filterultrassom(ultrassom)
	
	if (distancia < dist_max):  # Pode ser que o cubo esteja no último quadrado
		move_tank.on(SpeedPercent(50), SpeedPercent(50))
		while(distancia > 300 and flag != 2):  # Verifica se achou cubo de outra linha

			if(flag):
				ultravalue = filterultrassom(ultrassom)
				flag = 0 # Estado 1
			else:
				flag = 1 # Estado 2
			if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK and distancia > 320):
				# Alinhamento
				alinhaTempo(colorE, colorD, 40, move_tank, False)
				ultravalue = filterultrassom(ultrassom)

			distancia = filterultrassom(ultrassom)
			if(abs(distancia-ultravalue) > 200):
				flag = 2 # Não existe cubo na linha

		distancia = filterultrassom(ultrassom)

		# Se existe algo em 2100 mm e não deu erro. Tem cubo!
		if(filterultrassom(ultrassom) < 2100 and flag != 2):
			return True
		else:
			# Se deu ruim, dá ré
			move_tank.on(SpeedPercent(-50), SpeedPercent(-50))
			while(motorDir.position - distMotor > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					alinhaTempo(colorE, colorD, 40, move_tank, True)

	# Se chegou no fim, não precisa virar para procurar
	if(linha != 7):
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.0)
	return False
