from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from statistics import mode
from support import *
from alinhamentoTempo import alinhaTempo

#Definindo o nome das cores da matriz de cores
Preto = 0
Branco = 1

#Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

#Disponibilidade
Livre = True
Ocupada = False

#Fatores
N = 804
VEL = 40
VELROT = 30
STOP = SpeedPercent(0)
ROT90 = 1.03
ROT180 = 2.05
DISTPAREDE = 90
QUADRADO = 2.252

def leArquivo():
	coresLavanderias = [[1 for i in range(2)] for j in range(2)] # Todas lavanderias iniciam brancas
	arq = open('cores.txt', 'r')
	texto = arq.read().split()
	coresLavanderias[0][0] = int(texto[0])
	coresLavanderias[0][1] = int(texto[1])
	coresLavanderias[1][0] = int(texto[2])
	coresLavanderias[1][1] = int(texto[3])
	arq.close()
	return coresLavanderias

def escreveArquivo(coresLavanderias):
	arq = open('cores.txt', 'w')
	arq.write(str(coresLavanderias[0][0])+" "+str(coresLavanderias[0][1])+" "+str(coresLavanderias[1][0])+" "+str(coresLavanderias[1][1]))
	arq.close()

def lateralDisponivel(lavanderias):
	if lavanderias[0][0] == 1 and lavanderias[1][0] == 1:
		# lavanderias esquerda
		lateral = 1
	elif lavanderias[1][0] == 1 and lavanderias[1][1] == 1:
		# lavanderias de baixo
		lateral = 2
	elif lavanderias[1][1] == 1 and lavanderias[0][1] == 1:
		# lavanderias direita
		lateral = 3
	elif lavanderias[0][1] == 1 and lavanderias[0][0] == 1:
		# lavanderias de cima
		# é mais possíVEL achar um dos cubos que falta mas o intuitivo seria ir pra 4
		lateral = 3
	elif lavanderias[0][0] == 1 and lavanderias[1][1] == 1:
		# superior esquerda e inferior direita
		# cuidado
		lateral = 4
	elif lavanderias[1][0] == 1 and lavanderias[0][1] == 1:
		# inferior esquerda e superior direita
		lateral = 4
	else:
		# Só existe uma lavanderia sem cubo
		# ir para lateral 4 e começar a procurar um cubo
		# chamar função de achar um cubo
		lateral = 4
	return lateral

def reiniciar(disponibilidade, lateral, move_tank, lavanderias, ultrassom, colorE, colorD):
	if lateral == 1:
		# 180º
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180)
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(STOP, STOP)
		# para na lavanderia da lavanderia 1 e vira para iniciar
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180)

	elif lateral == 2:
		# 180º
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180)
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(STOP, STOP)
		# chegou na lavanderia da lateral 2 (90º)
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)
		
		# subindo a lateral
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(STOP, STOP)
		# 180ºcv f hmjklmyjrvwt (ass: Bianca)
		# chegou na [1][1]
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180)
	
	elif lateral == 3:
		contLinha = 0
		move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
		# segue reto
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while contLinha < 7:
			if (filterultrassom(ultrassom)) <= DISTPAREDE:
				#contornar
				move_tank.on(STOP, STOP)
				move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
				move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), QUADRADO)
				move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)
				move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
				contLinha += 1
		# chegamos na lateral 3
		move_tank.on(STOP, STOP)
		move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 0.1)
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)
		# direcionando para a lavanderia
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(STOP, STOP)
		# chegamos na [0][1]
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180)

	elif lateral == 4:
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		if lavanderias[0][0] == 0:
			# desviando do cubo
			move_tank.on(STOP, STOP)
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
			drift(False, move_tank)
		else:
			move_tank.on(STOP, STOP)
			# chegou na lavanderia da lateral 4 (90º)
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)		
	
	# após chegar na lateral reinicia suas funcionalidades
	numCubos = disponibilidade.count(0)
	coresLavanderias = leArquivo()
	return numCubos, coresLavanderias

def iniciar(move_tank, ultrassom, colorE, colorD, coresLavanderias):
	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
	
	while True:
		# Filtrando o valor do ultrassom
		distancia = 0
		contador = 0

		while(contador < 5):
			distancia += ultrassom.value()
			contador += 1
		distancia = int(distancia/5)

		print("ultrassom: ", distancia)

		# Direcionando-se à primeira lavanderia

		if(distancia <= 125):
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)

			# Filtro para cor de leitura #
			colorListE = list()
			colorListD = list()
			contador = 0
			while(contador < 3):
				colorListE.append(colorE.value())
				colorListD.append(colorD.value())
				contador += 1
			print("moda esquerda: ", mode(colorListE))
			print("moda direita: ", mode(colorListD))

			if mode(colorListE) == COLOR_WHITE:
				corEsq = COLOR_WHITE
			else:
				corEsq = COLOR_BLACK
			if mode(colorListD) == COLOR_WHITE:
				corDir = COLOR_WHITE
			else:
				corDir = COLOR_BLACK
			############################ Finalizando filtro ############################

			# Definindo a matriz de cores tendo em vista que ela foi iniciada totalmente preta
			print("dir: ", colorD.value())
			print("esq: ", colorE.value())
			print("ultrassom: ", ultrassom.value())

			# Preto
			if(corEsq == corDir and corEsq != COLOR_WHITE):
				print('op1')
				coresLavanderias[0][1] = Branco
				coresLavanderias[1][0] = Branco
				break
			# Branco
			elif(corEsq == corDir and corEsq != COLOR_BLACK):
				print('op2')
				coresLavanderias[0][0] = Branco
				coresLavanderias[1][1] = Branco
				break

		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and distancia > 310):
			alinhaTempo(colorE, colorD, 40, move_tank, False)

	escreveArquivo(coresLavanderias)
	return coresLavanderias

def setRobot(lavanderias, disponibilidade):
	# Inicialização de motores
	move_garra = MoveTank(OUTPUT_A, OUTPUT_B, motor_class=MediumMotor)
	move_tank = MoveTank(OUTPUT_C, OUTPUT_D)

	# Inicialização de sensores
	ultrassom = UltrasonicSensor(INPUT_1)
	colorF = ColorSensor(INPUT_2)
	colorE = ColorSensor(INPUT_3)
	colorD = ColorSensor(INPUT_4)
	colorE.mode = 'COL-COLOR'
	colorD.mode = 'COL-COLOR'

	numCubos = 0
	coresLavanderias = [[Preto for i in range(2)] for j in range(2)] # Todas lavanderias iniciam pretas
 ##

	if disponibilidade[0] == '1' and disponibilidade[1] == '1' and disponibilidade[2] == '1' and disponibilidade[3] == '1':
		lateral = 4
		coresLavanderias = iniciar(move_tank, ultrassom, colorE, colorD, coresLavanderias)
	else:
		lateral = lateralDisponiVEL(lavanderias)
		numCubos, coresLavanderias = reiniciar(disponibilidade, lateral, move_tank, lavanderias, ultrassom, colorE, colorD)
	
	return move_garra, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias, lateral, numCubos
