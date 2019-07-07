#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

def threeVal(sensor):
	"Pega 3 leituras do sensor e retorna a cor predominante"
	#op = Operacao (esquerda ou direita)
	cont = 0 #contador
	preto = 0
	branco = 0
	 #Verificar o valor do sensor da esquerda
	while(cont < 3):
		cont += 1
		valor = sensor.value()
		if(valor == COLOR_WHITE):
			branco += 1
		elif(valor == COLOR_BLACK):
			preto += 1

	print(preto, branco)
	return COLOR_BLACK if (preto > branco) else COLOR_WHITE

def alinhaPosicao():
	# Definindo valores de leitura do ColorSensor
	COLOR_BLACK = 1
	COLOR_WHITE = 6

	colorsenseE = ColorSensor(INPUT_3) #Cor Esquerda
	colorsenseD = ColorSensor(INPUT_4) #Cor Direita
	colorsenseD.mode = 'COL-COLOR' #Muda de LUz para Cor
	colorsenseE.mode = 'COL-COLOR'

	passo = 0 #Identifica se passou da linha ou ainda não

	motoresq = LargeMotor(OUTPUT_B)
	motordir = LargeMotor(OUTPUT_D)
	tank_drive = MoveTank(OUTPUT_B, OUTPUT_D) #Controle mutuo dos motores
	tank_drive.on(SpeedPercent(20),SpeedPercent(20)) #Inicia o movimento
	actime = time.clock() #Pega o tempo atual (So pra parar depois de x segundos)

	while True:
		leftColor =	colorsenseE.value()
		rightColor = colorsenseD.value()

		print(leftColor, " Esquerda")
		print(rightColor, " Direita")
		print(passo, " Passo")

		if (leftColor == COLOR_BLACK and rightColor == COLOR_WHITE):
			#Chegou na linha com o lado esquerdo primeiro
			if (passo == 0):
				#Esta chegando, nao saindo
				while (rightColor == COLOR_WHITE and leftColor == COLOR_BLACK):
					# Movimentar o lado do pivô para sair da linha (3)
					tank_drive.on(SpeedPercent(3),SpeedPercent(20)) #Pivo do lado esquerdo
					leftColor = threeVal(colorsenseE)
					rightColor = threeVal(colorsenseD)
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
					# Movimentar o lado do pivô para sair da linha (3)
					tank_drive.on(SpeedPercent(20),SpeedPercent(3))
					leftColor =	threeVal(colorsenseE)
					rightColor = threeVal(colorsenseD)
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

if __name__ == '__main__':
	alinhaPosicao()
