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

def acharHome(ultra, drive, color):
	"Acha o primeiro quadrado e define a posição atual"
	dist = ultra.value()
	drive.on(SpeedPercent(VELOC_BASE),SpeedPercent(VELOC_BASE))
	
	while dist > 170: 
		dist = ultra.value()
		print("Procurando parede")
		print(dist)

	drive.off()
	cor = color.value() #Sensor pra ver a cor da lavanderia
	return cor

def percorreArena(arena, posiAt, posiAn, ultra, motorEsq, motorDir, sensorEsq, sensorDir):
	"Percorre a borda do grid, para achar os cubos. Retorna a arena completa."
	achar = 0 #Sensor de distância, verficar cubos
	numBlocos = -1 #Quantos blocos foram encontrados
	posiBlocos = [[0] * 2 for i in range(4)] #4 Vetores de 2 '0's cada
	distMotores = 0 #Quanto o motor rotacionou
	tank_drive = MoveTank(OUTPUT_C, OUTPUT_D)
	distUAn = 2250 #Distância medida anteriormente pelo Ultrassom
	andandoEm = 0 #0 - X, 1 - Y
	deveProcurar = 0

	while numBlocos < 4:
		#Percorre em círculos até achar todos
		distU = ultra.value()
		deveProcurar = 0

		if (posiAt[1] == TAMANHO_ARENA or posiAt[1] == 0) and distU < 150:
			#O fim da arena sempre ocorre em X = 0 ou X = 7
			#Chegou no fim, virar e continuar
			while(distU > 120):
				distU = ultra.value()
			tank_drive.on_for_rotations(SpeedPercent(-VELOC_BASE),SpeedPercent(VELOC_BASE), ROTACAO) #Vira pra esquerda
			tank_drive.on_for_rotations(SpeedPercent(VELOC_BASE),SpeedPercent(VELOC_BASE), 2.252)  #Avança

			posiAn[0] = posiAt[0] if (posiAt[0] != posiAn[0]) else posiAt[1]
			#Se estou andando em Y, quando virar o Y se manterá até a próxma parede
			#Se estou andando em X, agora o Y deve aumentar ou diminuir (baseado no X atual)
			if(posiAt[0] != posiAn[0]): posiAt[0] = posiAn[1]

			posiAn[1] = posiAt[1] if (posiAt[1] != posiAn[1]) else (TAMANHO_ARENA - posiAt[0])
			#Se estou andando em X, quando virar o X se manterá até a próxima parede
			#Se estou andando em Y, agora o X deve aumentar ou diminuir (baseado no Y atual)
			if(posiAt[1] != posiAn[1]): posiAt[1] = (TAMANHO_ARENA) - posiAn[0]

		motorEsq.reset()
		motorDir.reset()
		distU = ultra.value()
		distUAn = distU
		corEsq = sensorEsq.value()
		corDir = sensorDir.value()
		tank_drive.on(SpeedPercent(VELOC_BASE),SpeedPercent(VELOC_BASE))

		while(distMotores < 300 ):#or (distUAn - distU) < 300): #Anda um quadrado

			distMotores = int((motorEsq.position + motorDir.position)/2)
			distU = ultra.value()
			if(corEsq == COLOR_BLACK or corDir == COLOR_BLACK):
				print("Checa")
				#Funcao checa alinhamento
			corEsq = sensorEsq.value()
			corDir = sensorDir.value()

		if posiAt[1] < posiAn[1]:
			#Andando até Y = 0
			posiAn[1] = posiAt[1]
			posiAt[1] -= 1
			andandoEm = 1
		elif posiAt[1] > posiAn[1]:
			#Andando até Y = 7
			posiAn[1] = posiAt[1]
			posiAt[1] += 1
			andandoEm = 1

		if posiAt[0] < posiAn[0]:
			#Andando até X = 0
			posiAn[0] = posiAt[0]
			posiAt[0] -= 1
			andandoEm = 0
		elif posiAt[0] > posiAn[0]:
			#Andando até X = 7
			posiAn[0] = posiAt[0]
			posiAt[0] += 1
			andandoEm = 0

		for i in range(TAMANHO_ARENA):
			#Verifica se existe ainda algum espaço não conhecido('0') na sequência observada
			if(andandoEm):
				#Andando em Y, verificar em X
				if(arena[posiAt[0]][i] == 0):
					deveProcurar = 1
			else:
				#Andando em X, verificar em Y
				if(arena[i][posiAt[1]] == 0):
					deveProcurar = 1
				

		if(deveProcurar):#Inicia o padrão
			tank_drive.on_for_rotations(SpeedPercent(-VELOC_BASE),SpeedPercent(VELOC_BASE), ROTACAO) #Vira pra esquerda
			distU = ultra.value()
			
			if(distU < ((300*TAMANHO_ARENA)-100)): #Achou algo...
				numBlocos += 1
				#VV Verifificar se o arrendondamento funciona direito
				if(posiAn[1] == posiAt[1]): #...enquanto andava em X
					correc = 0 if posiAt[0] else 1 #Correcao de +1 se viu a partir de um 0
					posiBlocos[numBlocos][1] = posiAt[1] #Está na posição X do robô
					posiBlocos[numBlocos][0] = abs(posiAt[0] - (int(distU / 300) + correc)) #Arredondamento da Distância em Y
					if(correc):
						#Como viu a partir de um 7, pintar de acordo
						for i in range(TAMANHO_ARENA - (posiBlocos[numBlocos][0] + 1)):
							arena[(TAMANHO_ARENA - i)][posiBlocos[numBlocos][1]] = 1
					else:
						#Como viu a partir de um 0, pintar de acordo
						for i in range(posiBlocos[numBlocos][0]):
							arena[i][posiBlocos[numBlocos][1]] = 1
				else: #...enquanto andava em Y
					correc = 0 if posiAt[1] else 1 #Correcao de +1 se viu a partir de um 0
					posiBlocos[numBlocos][0] = posiAt[0] #Está na posição Y do robô
					posiBlocos[numBlocos][1] = abs(posiAt[1] - (int(distU / 300) + correc)) #Arredondamento da Distância em X
					if(correc):
						#Como viu a partir de um 7, pintar de acordo
						for i in range(TAMANHO_ARENA - (posiBlocos[numBlocos][1] + 1)):
							arena[posiBlocos[numBlocos][0]][(TAMANHO_ARENA - i)] = 1
					else:
						#Como viu a partir de um 0, pintar de acordo
						for i in range(posiBlocos[numBlocos][1]):
							arena[posiBlocos[numBlocos][1]][i] = 1
				if(numBlocos >= 0):
					if(arena[posiBlocos[numBlocos][1]][posiBlocos[numBlocos][0]] == 2):
						#Achou um bloco que já tinha achado (Inútil?) (Atrapalha?)
						numBlocos -= 1
					else:
						arena[posiBlocos[numBlocos][1]][posiBlocos[numBlocos][0]] = 2
				else:
					arena[posiBlocos[numBlocos][1]][posiBlocos[numBlocos][0]] = 2
			else:
				for i in range(TAMANHO_ARENA):
					if(andandoEm):
						#Estava olhando a sequência Y
						arena[i][posiAt[1]] = 1
					else:
						#Estava olhando a sequência X
						arena[posiAt[0]][i] = 1
			tank_drive.on_for_rotations(SpeedPercent(VELOC_BASE),SpeedPercent(-VELOC_BASE), ROTACAO) #Vira pra direita

	for i in range(TAMANHO_ARENA):
		for j in range(TAMANHO_ARENA):
			#Limpa os espaços restantes na arena
			if(arena[i][j] == 0):
				arena[i][j] = 1

	arena[posiAt[0]][posiAt[1]] = 3 #Marca a posição do robô
	return arena

def main():
	ultraSense = UltrasonicSensor(INPUT_1)
	sensorFrente = ColorSensor(INPUT_2)
	sensorEsq = ColorSensor(INPUT_3)
	sensorDir = ColorSensor(INPUT_4)
	motorEsq = LargeMotor(OUTPUT_C)
	motorDir = LargeMotor(OUTPUT_D)
	tank_drive = MoveTank(OUTPUT_C, OUTPUT_D)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

	arena = [[0] * (TAMANHO_ARENA+1) for i in range(TAMANHO_ARENA+1)]
	posi_at = [TAMANHO_ARENA,1] #y,x
	posi_an = [TAMANHO_ARENA,0]
	motorEsq.reset()
	motorDir.reset()

	corInicial = acharHome(ultraSense, tank_drive, sensorEsq)
	print(corInicial)
	tank_drive.on_for_rotations(SpeedPercent(-VELOC_BASE),SpeedPercent(VELOC_BASE), ROTACAO) #Vira pra esquerda
	tank_drive.on_for_rotations(SpeedPercent(VELOC_BASE),SpeedPercent(VELOC_BASE), 2.252)  #Avança
	arena = percorreArena(arena, posi_at, posi_an, ultraSense, motorEsq, motorDir, sensorEsq, sensorDir)

main()

tank_drive.on(SpeedPercent(0),SpeedPercent(0))
