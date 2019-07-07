#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

# Definindo valores de leitura do ColorSensor
COLOR_BLACK = 1
COLOR_WHITE = 6

def threeVal(op):
	"Pega 3 leituras do sensor e retorna a cor predominante"
	#op = Operacao (esquerda ou direita)
	cont = 0 #contador
	preto = 0
	branco = 0

	if(op == 'd'): #Verificar o valor do sensor da direita
		while(cont < 3):
			cont += 1
			valor = colorsenseD.value()
			if(valor == COLOR_WHITE):
				branco += 1
			elif(valor == COLOR_BLACK):
				preto += 1

	elif(op == 'e'): #Verificar o valor do sensor da esquerda
		while(cont < 3):
			cont += 1
			valor = colorsenseE.value()
			if(valor == COLOR_WHITE):
				branco += 1
			elif(valor == COLOR_BLACK):
				preto += 1

	print(preto, branco)
	return COLOR_BLACK if (preto > branco) else COLOR_WHITE

ultraSense = UltrasonicSensor(INPUT_1) #Distancia
colorsenseF = ColorSensor(INPUT_2) #Cor Frente
colorsenseE = ColorSensor(INPUT_3) #Cor Esquerda
colorsenseD = ColorSensor(INPUT_4) #Cor Direita
colorsenseD.mode = 'COL-COLOR' #Muda de LUz para Cor
colorsenseE.mode = 'COL-COLOR'

passo = 0 #Identifica se passou da linha ou ainda não

ultraSense.mode = 'US-DIST-CM' #Não funciona, a distancia continua em mm
motoresq = LargeMotor(OUTPUT_B)
motordir = LargeMotor(OUTPUT_D)
tank_drive = MoveTank(OUTPUT_B, OUTPUT_D) #Controle mutuo dos motores
tank_drive.on(SpeedPercent(20),SpeedPercent(20)) #Inicia o movimento
actime = time.clock() #Pega o tempo atual (So pra parar depois de x segundos)

while True:
	dist = ultraSense.value()
	frontColor = colorsenseF.value()
	leftColor =	colorsenseE.value()
	rightColor = colorsenseD.value()

	print(frontColor, " Frente")
	print(dist, " Ultrassom")
	print(leftColor, " Esquerda")
	print(rightColor, " Direita")
	print(passo, " Passo")

	if (leftColor == COLOR_BLACK and rightColor == COLOR_WHITE):
		#Chegou na linha com o lado esquerdo primeiro
		if (passo == 0):
			#Esta chegando, nao saindo
			while (rightColor == COLOR_WHITE and leftColor == COLOR_BLACK):
				tank_drive.on(SpeedPercent(1),SpeedPercent(20)) #Pivo do lado esquerdo
				leftColor = threeVal('e')
				rightColor = threeVal('d')
		#else:
		#	while (leftColor == COLOR_BLACK and rightColor != COLOR_BLACK):
		#		tank_drive.on(SpeedPercent(20),SpeedPercent(10))
		#		leftColor = fiveVal('e')
		#		rightColor = fiveVal('d')
		passo = 1

	print(leftColor, " Esquerda")
	print(rightColor, " Direita")

	if (leftColor == COLOR_WHITE and rightColor == COLOR_BLACK):
		if(passo == 0):
			while (leftColor == COLOR_WHITE and rightColor != COLOR_WHITE):
				tank_drive.on(SpeedPercent(20),SpeedPercent(1))
				leftColor =	threeVal('e')
				rightColor = threeVal('d')
		#else:
		#	while (rightColor == COLOR_BLACK and leftColor != COLOR_BLACK):
		#		tank_drive.on(SpeedPercent(10),SpeedPercent(20))
		#		leftColor = fiveVal('e')
		#		rightColor = fiveVal('d')
		passo = 1

	if (leftColor == COLOR_WHITE and rightColor == COLOR_WHITE and passo ==1):
		passo = 0
		print("Zerou o Passo")

	leftColor = colorsenseE.value()
	rightColor = colorsenseD.value()

	if(leftColor == COLOR_WHITE and rightColor == COLOR_WHITE) or (leftColor == COLOR_BLACK and rightColor == COLOR_BLACK):
		#Se ele está no branco ou dentro da faixa, segure reto.
		tank_drive.on(SpeedPercent(20),SpeedPercent(20))
	ntime = time.clock() - actime
	if(ntime > 5):
		#Acaba em 5s
		break


tank_drive.on(SpeedPercent(0),SpeedPercent(0))
