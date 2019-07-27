#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

# Definindo valores de leitura do ColorSensor
COLOR_BLACK = 1
COLOR_WHITE = 6
# Definindo variaveis globais para mudar mais facil
TAMANHO_ARENA = 7	# Numero de espacos na arena (Do zero)
ROTACAO = 1	# Quanto as rodas precisam rodar juntas pro robo girar 90 graus
VELOC_BASE = 20		# A porcentagem de velocidade base dos motores

def pegaBloco(garra1, garra2, tank_drive,lateral, coresLavanderias, lavanderias, sensorFrontal):
	garra1.on_for_rotations(SpeedPercent(10), 0.2) #garra da esquerda abre
	garra2.on_for_rotations(SpeedPercent(-10), 0.2) #garra da direita abre
	tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(20), 0.65) #movimenta com base em 125mm de distância do cubo
	garra1.on_for_rotations(SpeedPercent(-10), 0.2) #garra da esquerda fecha
	garra2.on_for_rotations(SpeedPercent(10), 0.2) #garra da direita fecha

def largaBloco(garra1, garra2, tank_drive):
	garra1.on_for_rotations(SpeedPercent(10), 0.2) #garra da esquerda abre
	garra2.on_for_rotations(SpeedPercent(-10), 0.2) #garra da direita abre
	tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.65) #ré com base em 125mm de distância do cubo
	garra1.on_for_rotations(SpeedPercent(-10), 0.2) #garra da esquerda fecha
	garra2.on_for_rotations(SpeedPercent(10), 0.2) #garra da direita fecha

def verificaBloco(sensorFrontal):
	# Filtro de verificação da cor do cubo
	cont = 0
	cor = 0
	while cont < 3:
		cor += sensorFrontal.value()
		cont +=1
	cor = cor/3
	##########################################

def percorreArena(posiAt, posiAn, ultra, motorEsq, motorDir, sensorEsq, sensorDir):
	"Percorre a borda do grid, para achar os cubos. Retorna a arena completa."
	achar = 0 #Sensor de distância, verficar cubos
	numBlocos = -1 #Quantos blocos foram encontrados
	distMotores = 0 #Quanto o motor rotacionou
	tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)
	distUAn = 2250 #Distância medida anteriormente pelo Ultrassom
	deveProcurar = 1

	while numBlocos < 4:
		#Percorre em círculos até achar todos
		distU = ultra.value()
		deveProcurar = 0

		motorEsq.reset()
		motorDir.reset()
		distMotores = 0
		corEsq = sensorEsq.value()
		corDir = sensorDir.value()
		tank_drive.on(SpeedPercent(VELOC_BASE),SpeedPercent(VELOC_BASE))

		while(distMotores < 600 ):
			distMotores = int((motorEsq.position + motorDir.position)/2)
			if(corEsq == COLOR_BLACK or corDir == COLOR_BLACK):
				print("Checa")
				#Funcao checa alinhamento
			corEsq = sensorEsq.value()
			corDir = sensorDir.value()
				
		if(deveProcurar):#Inicia o padrão
			tank_drive.on_for_rotations(SpeedPercent(-VELOC_BASE),SpeedPercent(VELOC_BASE), ROTACAO) #Vira pra esquerda
			distU = ultra.value()

			if(distU < ((300*TAMANHO_ARENA)-100)): #Achou algo...
				numBlocos += 1
				distUAn = distU
				tank_drive.on(SpeedPercent(VELOC_BASE),SpeedPercent(VELOC_BASE))
				while(distU > 125):
					if(corEsq == COLOR_BLACK or corDir == COLOR_BLACK):
						print("Checa")
						#Funcao checa alinhamento
					corEsq = sensorEsq.value()
					corDir = sensorDir.value()
					distU = ultra.value()
				tank_drive.on(SpeedPercent(0),SpeedPercent(0))
				pegaBloco()#PARAMETROS
				cor = verificaBloco()#PARAMETROS
				motorEsq.reset()
				motorDir.reset()
				while(distUAn - (distMotores/2) > 0):
					#Dar ré até chegar na parede
				tank_drive.on_for_rotations(SpeedPercent(VELOC_BASE),SpeedPercent(-VELOC_BASE), ROTACAO) #Vira pra direita
				#Andar até chegar na lavanderia(Vamos ter que marcar a posicao atual de qualquer jeito)
				#Verficar se a cor da lavanderia é a mesma que o cubo
					#Se sim, largaBloco()
					#Se não, continuar até chegar na próxima lavanderia
			else:
				tank_drive.on_for_rotations(SpeedPercent(VELOC_BASE),SpeedPercent(-VELOC_BASE), ROTACAO) #Vira pra direita

	return True


def main():
	tank_drive = MoveTank(OUTPUT_C, OUTPUT_D)  
	ultrassom = UltrasonicSensor(INPUT_1)
	garra1 = Motor(OUTPUT_A)
	garra2 = Motor(OUTPUT_B)
	sensorFrontal = ColorSensor(INPUT_2)
	sensorFrontal.MODE_RGB_RAW
