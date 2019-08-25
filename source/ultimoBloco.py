from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from garra import *

#Define Vars
N = 804
VEL = 40
STOP = SpeedPercent(0)
ROT90 = 1.03

def ultimoBloco(linha, lavanderias, lateral, move_tank, distRodas, garra_drive, motorDir):
	"Pega o ultimo bloco ignorando o resto dos comandos para levar para a ultima lavanderia desocupada"
	motorDir.reset()

	# Inicia quando já está com o cubo preso na garra
	# Baseado na lateral atual do robô
	# Depois de verificar qual lavanderia está livre, se movimenta até ela pelo meio da arena.
	if(lateral == 1): 
		if(lavanderias[0][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[0][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
	elif(lateral == 2):
		if(lavanderias[0][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[0][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		if(lavanderias[0][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[0][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
	elif(lateral == 4):
		if(lavanderias[0][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[0][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				pass
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha

	motorDir.reset()
	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) #Vai até a lavanderia

	while(motorDir.position < (x*N + 200)):
		#Enquanto, a partir da linha que se encontrava o robô, não chega na lavanderia, avança.
		pass
	move_tank.on(STOP, STOP)
	largaBloco(garra_drive, move_tank)
	#Acabou. 
	return