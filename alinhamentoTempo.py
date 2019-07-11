#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

def alinhaTempo(sensorE, sensorD, velocidade, tank_drive):

	#Definindo motores
	#tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)

	# Definindo valores de leitura do ColorSensor
	COLOR_BLACK = 1
	COLOR_WHITE = 6

	# Inicializando as variaveis de tempo
	leftTime = 0
	rightTime = 0
	iniTime = 0
	totaleftTime = 0
	totalrightTime = 0

	#Inicializando as variaveis dos sensores de cor
	leftColor = sensorE.value()
	rightColor = sensorD.value()

	sensorE.mode = 'COL-COLOR' #Muda de Luz para Cor
	sensorD.mode = 'COL-COLOR'

	#tank_drive.on(SpeedPercent(velocidade),SpeedPercent(velocidade)) #Inicia o movimento

	leftColor = sensorE.value()
	rightColor = sensorD.value()
	SAngle = False
	# if(leftColor == COLOR_BLACK and rightColor == COLOR_WHITE): 
	# 	print("ENTROU")
	# 	rightTime = time.clock()
	# 	leftTime = time.clock()
	# 	iniTime = time.clock()

	# 	while(leftColor==COLOR_BLACK or rightColor == COLOR_BLACK):
	# 		leftColor = sensorE.value()
	# 		rightColor = sensorD.value()

	# 		if(leftColor==COLOR_WHITE):
	# 			# Esquerda passou a linha preta - Tempo de saída da esquerda
	# 			leftTime = time.clock()
	# 			SAngle = True

	# 	# Ao sair do while direita passou linha preta (em SAngle)
		
	# 	# Ângulos pequenos
	# 	if(SAngle):
	# 		rightTime = time.clock()

	# 	else:
	# 		leftTime = time.clock()
	# 		while(rightColor==COLOR_WHITE):
	# 			rightColor = sensorD.value()
			
	# 		while(rightColor == COLOR_BLACK):
	# 			rightColor = sensorD.value()
	# 		rightTime = time.clock()
	# 	totaleftTime = (rightTime - iniTime) - (leftTime - iniTime)

	# 	ajusteTime = time.clock()
	# 	while(time.clock()-ajusteTime < int(totaleftTime*2)):
	# 		print("algumacoisa")
	# 		print(totaleftTime)
	# 		tank_drive.on(SpeedPercent((velocidade/2)), SpeedPercent(velocidade))
		
	# 	tank_drive.on(SpeedPercent((velocidade)), SpeedPercent(velocidade))

	# Verificando a direita chegando primeiro no preto

	if(rightColor == COLOR_BLACK and leftColor == COLOR_WHITE):
		print("ENTROU2")
		rightTime = time.clock()
		leftTime = time.clock()
		iniTime = time.clock()

		while(leftColor!=COLOR_WHITE or rightColor != COLOR_WHITE):
			newtime = time.clock()
			print("While 2")

			if(rightColor!=COLOR_BLACK and SAngle == False):
				print("PASSOU")
				# Direita passou a linha preta - Tempo de saída da direita
				rightTime = time.clock()
				SAngle = True
			leftColor = sensorE.value()
			rightColor = sensorD.value()
			print(leftColor, "ESQUERDA")
			print(rightColor, "DIREITA")
			newtime = time.clock() - newtime
			print(newtime)

		# Ao sair do while esquerda passou linha preta (em SAngle)
		print(SAngle)
		# Ângulos pequenos
		if(SAngle):
			leftTime = time.clock()

		else:
			rightTime = time.clock()
			while(leftColor==COLOR_WHITE):
				leftColor = sensorE.value()
			
			while(leftColor == COLOR_BLACK):
				leftColor = sensorE.value()
			leftTime = time.clock()

		totalrightTime = (leftTime - iniTime) - (rightTime - iniTime)
		ajusteTime = time.clock()
		# Mudar a potência dos motores pelo dobro do tempo para alinhar
		# while(time.clock()-ajusteTime < int(totalrightTime*2)):
		# 	print(totalrightTime)
		# 	print("algumacoisa2")
			#tank_drive.on(SpeedPercent((velocidade)), SpeedPercent(velocidade/2))
	
		#tank_drive.on(SpeedPercent((velocidade)), SpeedPercent(velocidade))


if __name__ == '__main__':
	actime = time.clock()
	velocidade = 20

	colorsenseE = ColorSensor(INPUT_3) #Cor Esquerda
	colorsenseD = ColorSensor(INPUT_4) #Cor Direita

	motorE = LargeMotor(OUTPUT_B)
	motorD = LargeMotor(OUTPUT_D)
	tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)
	#tank_drive.on(SpeedPercent(velocidade),SpeedPercent(velocidade))
	while True:
		alinhaTempo(colorsenseE, colorsenseD, velocidade, tank_drive)
		ntime = time.clock() - actime
		if(ntime > 10):
			#Acaba em 10s
			break
	motorE.off()
	motorD.off()