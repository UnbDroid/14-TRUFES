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
N = 780

def descerLateral(move_tank, motorEsq, motorDir, ultrassom, colorE, colorD):

	motorEsq.reset()
	motorDir.reset()
	distMotores = 0
	
	# Desce a lateral com base em N, que é a distância de um quadrado
	# move_tank.on(SpeedPercent(40), SpeedPercent(40))
	# while(N - distMotores > 0):
	# 	distMotores = int((motorEsq.position + motorDir.position)/2)
	# 	# Faz o alinhamento
	# 	if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
	# 		alinhaTempo(colorE, colorD, 40, move_tank, False)
	# move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.04) # Vira 90º à esquerda
	# move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 0.07) # Ajuste do erro de ré

	move_tank.on(SpeedPercent(40), SpeedPercent(40))
	while(True):
		# Faz o alinhamento
		if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
			motorDir.reset()
			motorEsq.reset()
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			alinhaTempo(colorE, colorD, 40, move_tank, False)
			break
	while(580 - distMotores > 0):
	 	distMotores = int((motorEsq.position + motorDir.position)/2)
	 	# Faz o alinhamento	
	move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.04) # Vira 90º à esquerda
	move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 0.07) # Ajuste do erro de ré


def verificaLinha(move_tank, ultrassom, colorE, colorD, motorEsq, motorDir, linha):
	distancia = 0
	ultravalue = 0
	correction = 0
	flag = 1
	distMotor = int((motorDir.position + motorEsq.position)/2)
	distancia = filterultrassom(ultrassom)

	print(distMotor)
	if (distancia < dist_max):  # Pode ser que o cubo esteja no último quadrado
		move_tank.on(SpeedPercent(50), SpeedPercent(50))
		while(distancia > 300 and flag != 2):  # Verifica se achou cubo de outra linha
			print("Primeira: ", motorDir.position)
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
			print(distancia)
			if(abs(distancia-ultravalue) > 200 or distancia > 1840):
				print("Dist", distancia)
				print("Ultra:", ultravalue)
				flag = 2 # Não existe cubo na linha

		distancia = filterultrassom(ultrassom)

		# Se existe algo em 2100 mm e não deu erro. Tem cubo!
		if(filterultrassom(ultrassom) < 2100 and flag != 2):
			return True
		else:
			# Se deu ruim, dá ré
			print("Segunda: ", int((motorDir.position + motorEsq.position)/2))
			move_tank.on(SpeedPercent(-50), SpeedPercent(-50))
			posiMotor = int((motorDir.position + motorEsq.position)/2)
			while((abs(posiMotor) - distMotor) > 160):
				if((int((motorDir.position + motorEsq.position)/2) < 0 and posiMotor > 0) or (int((motorDir.position + motorEsq.position)/2) > 0 and posiMotor < 0)):
					break
				posiMotor = int((motorDir.position + motorEsq.position)/2)
				print("N:", posiMotor)
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					alinhaTempo(colorE, colorD, 40, move_tank, True)
			correction = 0.1


	# Se chegou no fim, não precisa virar para procurar
	if(linha != 7):
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1 + correction)
	return False
