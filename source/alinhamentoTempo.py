#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

def alinhaTempo(sensorE, sensorD, velocidade, tank_drive, re):

	#Definindo motores
	#tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)

	# Definindo valores de leitura do ColorSensor
	COLOR_BLACK = 1
	COLOR_WHITE = 6

	# Inicializando as variaveis de tempo
	leftTime = 0
	rightTime = 0

	#Inicializando as variaveis dos sensores de cor
	leftColor = sensorE.value()
	rightColor = sensorD.value()

	iniTime = time.clock()

	# Define se irá de ré ou para frente com base no booleano 're', alterando a velocidade pra positivo ou negativo
	velocidade = -velocidade if (re) else velocidade 
	print(velocidade)

	# Verifica o momento que os sensores passaram nas linhas pretas, essa verificação é feita por 0.7 segundos
	while((time.clock() - iniTime) < 0.7):
		leftColor = sensorE.value()
		rightColor = sensorD.value()
		if(leftColor == COLOR_BLACK):
			leftTime = time.clock()
			#print(leftTime, "LEFT")
		if(rightColor == COLOR_BLACK):
			rightTime = time.clock()
			#print(rightTime, "RIGHT")

	if(((leftTime + rightTime) - iniTime*2) > 0.55 or abs(leftTime-rightTime) > 3):
		print("WELP")
		pass
	elif(leftTime - iniTime > 0.5):
		#Encontrou linha lateral esquerda
		tank_drive.on_for_seconds(SpeedPercent(velocidade), SpeedPercent(velocidade/2), 0.1) 
		tank_drive.on(SpeedPercent(velocidade), SpeedPercent(velocidade))
	elif(rightTime - iniTime > 0.5):
		#Encontrou linha lateral direita
		tank_drive.on_for_seconds(SpeedPercent(velocidade/2), SpeedPercent(velocidade), 0.1) 
		tank_drive.on(SpeedPercent(velocidade), SpeedPercent(velocidade))
	else:

		# Tira a diferença entre os motores compensando um dos motores pela metade da velocidade
		# Isso é feito pelo dobro do tempo da diferença em que os dois passaram pelas linhas
		if(leftTime > rightTime):
			# Menor time = sair primeiro
			print('left', leftTime-rightTime)
			fixedTime = 2*(leftTime-rightTime+0.03)
			tank_drive.on_for_seconds(SpeedPercent(velocidade), SpeedPercent(velocidade/2),fixedTime) 
			tank_drive.on(SpeedPercent(velocidade), SpeedPercent(velocidade))
		if(leftTime < rightTime):
			# Menor time = sair primeiro
			print('right', rightTime-leftTime)
			fixedTime = 2*(rightTime-leftTime+0.03)
			tank_drive.on_for_seconds(SpeedPercent(velocidade/2), SpeedPercent(velocidade), fixedTime)        
			tank_drive.on(SpeedPercent(velocidade), SpeedPercent(velocidade))
	print("OUT")

# Main para testar, fica alinhando até encontrar algum objeto a pelo menos 20cm de distância
if __name__ == '__main__':
	actime = time.clock()
	velocidade = 40

	colorsenseE = ColorSensor(INPUT_3) #Cor Esquerda
	colorsenseD = ColorSensor(INPUT_4) #Cor Direita

	ultrassom = UltrasonicSensor(INPUT_1)

	tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)
	tank_drive.on(SpeedPercent(velocidade),SpeedPercent(velocidade))
	while True:
		if(ultrassom.value() <= 200):
			print(distancia, "stop")
			break
		alinhaTempo(colorsenseE, colorsenseD, velocidade, tank_drive)
		ntime = time.clock() - actime
		'''if(ntime > 3):
			#Acaba em 10s
			break'''
		distancia = ultrassom.value()/10
		print("distancia: ", distancia)
	tank_drive.on(SpeedPercent(0),SpeedPercent(0))
	