#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

def acharHome(ultra, drive, color):
	"Acha o primeiro quadrado e define a posição atual"
	dist = ultra.value()
	drive.on(SpeedPercent(20),SpeedPercent(20))
	
	while dist > 190: #Aqui iria o sensor de distância
		dist = ultra.value()
		print("Procurando parede")
		print(dist)

	drive.off()
	cor = color.value() #Sensor pra ver a cor da lavanderia
	return cor

def percorreArena(arena, posiAt, posiAn):
	"Percorre a borda do grid, para achar os cubos"
	achar = 0 #sensor de distância, verficar cubos
	numBlocos = -1 #Quantos blocos foram encontrados
	posiBlocos = [[0] * 2 for i in range(4)]
	while numBlocos < 4:
		#Percorre em círculos até achar todos
		if (posiAt[1] == 7 or posiAt[1] == 0 or posiAt[0] == 7) and dist < 120:
			#Chegou no fim, virar e continuar
			tank_drive.on_for_rotations(SpeedPercent(-70),SpeedPercent(70), 0.666) #Vira pra esquerda
			tank_drive.on_for_rotations(SpeedPercent(70),SpeedPercent(70), 2.252)  #Avança

			posiAn[0] = posiAt[0] if (posiAt[0] != posiAn[0]) else posiAt[1]
			#Se estou andando em Y, quando virar o Y se manterá até a próxma parede
			#Se estou andando em X, agora o Y deve aumentar ou diminuir (baseado no X atual)
			if(posiAt[0] != posiAn[0]): posiAt[0] = posiAn[1]

			posiAn[1] = posiAt[1] if (posiAt[1] != posiAn[1]) else (7 - posiAt[0])
			#Se estou andando em X, quando virar o X se manterá até a próxima parede
			#Se estou andando em Y, agora o X deve aumentar ou diminuir (baseado no Y atual)
			if(posiAt[1] != posiAn[1]): posiAt[1] = 7 - posiAn[0]

		tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 2.252) #Anda um quadrado (Mudar: a execução tem que ocorrer independente do movimento)
		#TODO: Identificar também pelo cruzamento da faixa preta

		if posiAt[1] < posiAn[1]:
			#Andando até Y = 0
			posiAn[1] = posiAt[1]
			posiAt[1] -= 1
		else:
			#Andando até Y = 7
			posiAn[1] = posiAt[1]
			posiAt[1] += 1

		if posiAt[0] < posiAn[0]:
			#Andando até X = 0
			posiAn[0] = posiAt[0]
			posiAt[0] -= 1
		else:
			#Andando até X = 7
			posiAn[0] = posiAt[0]
			posiAt[0] += 1

		tank_drive.on_for_rotations(SpeedPercent(-70),SpeedPercent(70), 0.666) #Vira pra esquerda
		#TODO: Ignorar as fileiras já "zeradas" quando circula.
		if(dist < 2000): #Achou algo...
			numBlocos += 1
			#VV Verfificar se o arrendondamento funciona direito
			if(posiAn[1] == posiAt[1]): #...enquanto andava em X
				posiBlocos[numBlocos][1] = posiAt[1] #Está na posição X do robô
				posiBlocos[numBlocos][0] = int(dist / 300) + 1 #Arredondamento da Distância em Y
			else: #...enquanto andava em Y
				posiBlocos[numBlocos][0] = posiAt[0] #Está na posição Y do robô
				posiBlocos[numBlocos][1] = int(dist / 300) + 1 #Arredondamento da Distância em X
			for i in range(4):
				if(posiBlocos[i][0] == posiBlocos[numBlocos][0] and posiBlocos[i][1] == posiBlocos[numBlocos][1]):
					#Achou um bloco que já tinha achado (Inútil?)
					numBlocos -= 1

		tank_drive.on_for_rotations(SpeedPercent(70),SpeedPercent(-70), 0.666) #Vira pra direita



def main():
	ultraSense = UltrasonicSensor(INPUT_1)
	#colorfrente = ColorSensor(INPUT_2)
	coloresq = ColorSensor(INPUT_3)
	colordir = ColorSensor(INPUT_4)
	motoresq = LargeMotor(OUTPUT_B)
	motordir = LargeMotor(OUTPUT_D)
	tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

	arena = [[0] * 8 for i in range(8)]
	posi_at = [7,0] #y,x
	posi_an = [7,0]
	motoresq.reset()
	motordir.reset()

	corInicial = acharHome(ultraSense, tank_drive, coloresq)

main()
# tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(-40), 0.666)
# tank_drive.on_for_rotations(SpeedPercent(60),SpeedPercent(60), 0.5)
# tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(-40), 0.666)

# while a < 1200:
# 	a = motor1.position
#  	b = motor2.position
#  	andado = (a+b)/2
#tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 2.252*8)
# while achar != 1:
# 		if posi[1] == 7:
# 			tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(40), 0.666)
# 			tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 2.273)
# 			tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(40), 0.666)
# 			posi[0] -= 1
# 		elif posi[1] == 0:
#print(corInicial)
#tank_drive.on_for_rotations(SpeedPercent(90),SpeedPercent(90), 0.1)
#tank_drive.on(SpeedPercent(0),SpeedPercent(0))
#time.sleep(1)
#tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 0.2)
#tank_drive.on(SpeedPercent(25),SpeedPercent(0))
#time.sleep(1)
#tank_drive.on(SpeedPercent(0),SpeedPercent(0))

tank_drive.on(SpeedPercent(0),SpeedPercent(0))
	# delta = a - b  
	# potr -= delta*0.005+int_delta*0.0000034
	# potl += delta*0.005+int_delta*0.0000034

	# if potr > 50:
	# 	potr = 50
	# 	pass

	# if potl > 50:
	# 	potl = 50
	# 	pass

	# motor1.on(SpeedPercent(potr))
	# motor2.on(SpeedPercent(potl))

		
	# if a < (b + 18):
	# 	while a < (b + 18):
	# 		motor1.on(SpeedPercent(40))
	# 		motor2.on(SpeedPercent(37))
	# 		a = motor1.position
	# 		b = motor2.position
	# elif (b + 18) < a:
	# 	while (b + 18) < a:
	# 		motor1.on(SpeedPercent(37))
	# 		motor2.on(SpeedPercent(40))
	# 		a = motor1.position
	# 		b = motor2.position
	# else:
	# 	motor1.on(SpeedPercent(40))
	# 	motor2.on(SpeedPercent(40))
#print(s)
#tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50),0.1)
#tank_drive.on(SpeedPercent(0), SpeedPercent(0))
#tank_drive.on_for_rotations(SpeedPercent(40), SpeedPercent(40),1.67)
#tank_drive.on_for_rotations(SpeedPercent(-40), SpeedPercent(0),1.25)
#tank_drive.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 3.7)

