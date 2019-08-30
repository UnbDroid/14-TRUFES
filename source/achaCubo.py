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
dist_max = 1600  # Essa é a distância do primeiro ao último quadrado visivel da linha
N = 780
VEL = 40
VELROT = 30

def descerLateral(move_tank, motorEsq, motorDir, ultrassom, colorE, colorD, linha):

	motorEsq.reset()
	motorDir.reset()
	distMotores = 0
	flag = True
	
	# Desce a lateral com base em N, que é a distância de um quadrado
	# move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
	# while(N - distMotores > 0):
	# 	distMotores = int((motorEsq.position + motorDir.position)/2)
	# 	# Faz o alinhamento
	# 	if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
	# 		alinhaTempo(colorE, colorD, VEL, move_tank, False)
	# move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), 1.04) # Vira 90º à esquerda
	# move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(VELROT), 0.07) # Ajuste do erro de ré

	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
	
	if(linha == 1 and colorE.value() == COLOR_BLACK):
		print("EIOAJASDJIASJDSPJASJPDDSJAP")
		move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 2)
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
	else:
		while(True):
			# Faz o alinhamento
			if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
				motorDir.reset()
				motorEsq.reset()
				move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
				alinhaTempo(colorE, colorD, VEL, move_tank, False)
				break
			if(distMotores > 750):
				move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 0.6)
				flag = False
		while(580 - distMotores > 0 and flag):
		 	distMotores = int((motorEsq.position + motorDir.position)/2)
		 	# Faz o alinhamento	
	move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), 1.04) # Vira 90º à esquerda
	if(linha == 3):
		move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 1.2) # Ré alinhar
		move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 0.3) # Ajuste

	move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(VELROT), 0.07) # Ajuste do erro de ré


def verificaLinha(move_tank, ultrassom, colorE, colorD, motorEsq, motorDir, linha):
	distancia = 0
	ultravalue = 0
	correction = 0.03
	flag = 1
	distMotor = int((motorDir.position + motorEsq.position)/2)
	distancia = filterultrassom(ultrassom)
	listaDist = []
	media = 0

	print(distMotor)
	if (distancia < dist_max):  # Pode ser que o cubo esteja no último quadrado
		move_tank.on(SpeedPercent(VEL/4), SpeedPercent(VEL/4))
		for i in range(0,12):
			listaDist.append(filterultrassom(ultrassom))
		ultravalue = filterultrassom(ultrassom)
		if(ultravalue > 140):
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		media = int(sum(listaDist) / len(listaDist))
#		print("valor medio ultrassom: ", media)
#		print("lista: ", listaDist)
		print("ultravalue: ", ultravalue)
		while(ultravalue > 240 and flag != 2):  # Verifica se achou cubo de outra linha
			if(colorD.value() == COLOR_BLACK ):
				print("LINHA")
			ultravalue = filterultrassom(ultrassom)
#			print("ULTRA:" , ultravalue)
#			print("valor medio ultrassom: ", media)

			if(ultravalue in range((media-300), (media+300))):
				listaDist.pop(0)
				listaDist.append(ultravalue)
				media = int(sum(listaDist) / len(listaDist))
			else:
				flag = 2
				
			if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK and ultravalue > 280):
				# Alinhamento
				alinhaTempo(colorE, colorD, VEL, move_tank, False)
			ultravalue = filterultrassom(ultrassom)

		distancia = filterultrassom(ultrassom)

		# Se existe algo em 1800 mm e não deu erro. Tem cubo!
		if(filterultrassom(ultrassom) < 1800 and flag != 2):
			print("linha: ", linha)
			return True
		else:
			posiMotor = int((motorDir.position + motorEsq.position)/2)
			go = 130 if (posiMotor > 350) else 80
			# Se deu ruim, dá ré
			print("s2")
			print("Segunda: ", int((motorDir.position + motorEsq.position)/2))
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL))
			while(abs(posiMotor - distMotor) > go):
				if((int((motorDir.position + motorEsq.position)/2) < 0 and posiMotor > 0) or (int((motorDir.position + motorEsq.position)/2) > 0 and posiMotor < 0)):
					break
				posiMotor = int((motorDir.position + motorEsq.position)/2)
				print("N:", posiMotor)
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			correction = 0.1


	# Se chegou no fim, não precisa virar para procurar
	print("linha: ", linha)
	if(linha != 7):
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), 1 + correction)
	elif(flag != 2 and linha == 6):
		print("drift viradinha")
		move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), 1 + correction)
	return False
