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

def descerLateral(move_tank, motorEsq, motorDir, ultrassom, colorE, colorD, linha):

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
	
	if(linha == 1 and colorE == COLOR_BLACK):
		tank_drive.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 1.3)
		tank_drive.on(SpeedPercent(velocidade), SpeedPercent(velocidade))
	else:
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
	listaDist = []
	media = 0

	print(distMotor)
	if (distancia < dist_max):  # Pode ser que o cubo esteja no último quadrado
		move_tank.on(SpeedPercent(50), SpeedPercent(50))
		for i in range(0,9):
			listaDist.append(filterultrassom(ultrassom))
		media = int(sum(listaDist) / len(listaDist))
		while(distancia > 300 and flag != 2):  # Verifica se achou cubo de outra linha
			print("ULTRA:" , ultravalue)
			print("Primeira: ", motorDir.position)
			ultravalue = filterultrassom(ultrassom)
			if(ultravalue in range((media-250), (media+250))):
				listaDist.pop(0)
				listaDist.append(ultravalue)
				media = int(sum(listaDist) / len(listaDist))
			else:
				flag = 2	
				
			if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK and distancia > 320):
				# Alinhamento
				alinhaTempo(colorE, colorD, 40, move_tank, False)
			distancia = filterultrassom(ultrassom)

		distancia = filterultrassom(ultrassom)

		# Se existe algo em 2100 mm e não deu erro. Tem cubo!
		if(filterultrassom(ultrassom) < 2100 and flag != 2):
			return True
		else:
			posiMotor = int((motorDir.position + motorEsq.position)/2)
			go = 130 if (posiMotor > 350) else 80
			# Se deu ruim, dá ré
			print("s2")
			print("Segunda: ", int((motorDir.position + motorEsq.position)/2))
			move_tank.on(SpeedPercent(-50), SpeedPercent(-50))
			while(abs(posiMotor - distMotor) > go):
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
