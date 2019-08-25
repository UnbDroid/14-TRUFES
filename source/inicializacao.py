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
	# Lê uma linha com 4 inteiros e coloca na matriz de cores
	# 1 é branco e 0 é preto
	texto = arq.read().split()
	coresLavanderias[0][0] = int(texto[0])
	coresLavanderias[0][1] = int(texto[1])
	coresLavanderias[1][0] = int(texto[2])
	coresLavanderias[1][1] = int(texto[3])
	arq.close()
	# Retorna uma matriz com a relação das cores das matrizes na arena
	return coresLavanderias

def escreveArquivo(coresLavanderias):
	arq = open('cores.txt', 'w')
	# Registra a matriz de cores da lavanderia para caso de reinicialização do robô
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

def reiniciar(disponibilidade, lateral, move_tank, lavanderias, ultrassom, colorE, colorD, move_steering):
	if lateral == 1:
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180) # 180º direita
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False) # Alinhamento
		move_tank.on(STOP, STOP)
		# para na lavanderia da lavanderia 1 e vira para iniciar
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180) # 180º direita

	elif lateral == 2:
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180) # 180º direita
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				# Alinhamento
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(STOP, STOP)
		# Chegou na lavanderia da lateral 2 (90º)
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90) # 90º direita
		
		# Subindo a lateral
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				# Alinhamento
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(STOP, STOP)
		# Chegou na [1][1]
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180) # 180º direita
	
	elif lateral == 3:
		contLinha = 0
		move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
		# Segue reto
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while contLinha < 7:
			if (filterultrassom(ultrassom)) <= DISTPAREDE:
				# Contornar cubo
				move_tank.on(STOP, STOP)
				move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
				move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), QUADRADO)
				move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)
				move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				# Alinhamento
				alinhaTempo(colorE, colorD, 40, move_tank, False)
				contLinha += 1
		# Chegamos na lateral 3
		move_tank.on(STOP, STOP)
		move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 0.1)
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90) # 90º direita
		# Direcionando para a lavanderia
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(STOP, STOP)
		# Chegamos na [0][1]
		move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT180)

	elif lateral == 4:
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		while (filterultrassom(ultrassom)) >= DISTPAREDE:
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		if lavanderias[0][0] == 0:
			# Desviando do cubo
			move_tank.on(STOP, STOP)
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90) # 90º esquerda
			drift(False, move_tank, move_steering)
		else:
			move_tank.on(STOP, STOP)
			# Chegou na lavanderia da lateral 4 (90º)
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)	# 90º esquerda
	
	# Após chegar na lateral reinicia suas funcionalidades
	numCubos = disponibilidade.count(0)
	coresLavanderias = leArquivo()
	return numCubos, coresLavanderias

def iniciar(move_tank, ultrassom, colorE, colorD, coresLavanderias):
	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
	
	while True:
		# Filtrando o valor do ultrassom
		distancia = 0
		contador = 0

		distancia = filterultrassom(ultrassom)

		# Direcionando-se à primeira lavanderia ([0][0])

		if(distancia <= 125):
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90) # 90º esquerda

			# Filtro para cor de leitura #
			colorListE = list()
			colorListD = list()
			contador = 0
			while(contador < 3):
				colorListE.append(colorE.value())
				colorListD.append(colorD.value())
				contador += 1
			
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

			# Preto
			if(corEsq == corDir and corEsq != COLOR_WHITE):
				
				coresLavanderias[0][1] = Branco
				coresLavanderias[1][0] = Branco
				break
			# Branco
			elif(corEsq == corDir and corEsq != COLOR_BLACK):
				
				coresLavanderias[0][0] = Branco
				coresLavanderias[1][1] = Branco
				break

		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and distancia > 310):
			# Alinhamento
			alinhaTempo(colorE, colorD, 40, move_tank, False)

	escreveArquivo(coresLavanderias)
	return coresLavanderias

def setRobot(lavanderias, disponibilidade):
	# Inicialização de motores
	move_garra = MoveTank(OUTPUT_A, OUTPUT_B, motor_class=MediumMotor)
	move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
	move_steering = MoveSteering(OUTPUT_C, OUTPUT_D)

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
	# Caso inicial de rodada
	if disponibilidade[0] == '1' and disponibilidade[1] == '1' and disponibilidade[2] == '1' and disponibilidade[3] == '1':
		lateral = 4
		coresLavanderias = iniciar(move_tank, ultrassom, colorE, colorD, coresLavanderias)
	# Caso de reinicialização
	else:
		lateral = lateralDisponivel(lavanderias)
		numCubos, coresLavanderias = reiniciar(disponibilidade, lateral, move_tank, lavanderias, ultrassom, colorE, colorD, move_steering)
	
	return move_garra, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias, lateral, numCubos, move_steering
