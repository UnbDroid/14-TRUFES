#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

def alinhaTempo(sensorE, sensorD):

	# Definindo valores de leitura do ColorSensor
	COLOR_BLACK = 1
	COLOR_WHITE = 6

	#Inicializando as variaveis
	leftColor = sensorE.value()
	rightColor = sensorD.value()

	sensorE.mode = 'COL-COLOR' #Muda de Luz para Cor
	sensorD.mode = 'COL-COLOR'

	tank_drive = MoveTank(OUTPUT_B, OUTPUT_D) #Controle mutuo dos motores
	tank_drive.on(SpeedPercent(20),SpeedPercent(20)) #Inicia o movimento
	
	
	while True:
		flag = 0
		leftColor = sensorE.value()
		rightColor = sensorD.value()
		SAngle = 0

		if(leftColor == COLOR_BLACK and rightColor == COLOR_WHITE):
			rightTime = time.clock()
			leftTime = time.clock()
			iniTime = time.clock()

			while(leftColor==COLOR_BLACK or rightColor == COLOR_BLACK):
				leftColor = sensorE.value()
				rightColor = sensorD.value()

				if(leftColor==COLOR_WHITE):
					# Esquerda passou a linha preta - Tempo de saída da esquerda
					leftTime = time.clock()

				if(rightColor == COLOR_BLACK and flag == 0):
					SAngle = 1
			# Ao sair do while direita passou linha preta (SAngle)
			
			# Ângulos pequenos
			if(SAngle):
				rightTime = time.clock()

			else:
				while(rightColor==COLOR_WHITE):
					rightColor = sensorD.value()
				
				while(rightColor == COLOR_BLACK):
					rightColor = sensorD.value()
				rightTime = time.clock()

			totalTime = (rightTime - iniTime) - (leftTime - iniTime)


if __name__ == '__main__':
	colorsenseE = ColorSensor(INPUT_3) #Cor Esquerda
	colorsenseD = ColorSensor(INPUT_4) #Cor Direita

	motorE = LargeMotor(OUTPUT_B)
	motorD = LargeMotor(OUTPUT_D)

	alinhaTempo(sensorE, sensorD, motorE, motorD)