from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from garra import *

def ultimoBloco(linha, lavanderias, lateral, move_tank, distRodas, garra_drive, motorDir):
	motorDir.reset()

	if(lateral == 1):
		if(lavanderias[0][0] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][0] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
		elif(lavanderias[1][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
		elif(lavanderias[0][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha
	elif(lateral == 2):
		if(lavanderias[0][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][0] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][1] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
		elif(lavanderias[0][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
		if(lavanderias[0][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
		elif(lavanderias[1][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][1] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha
		elif(lavanderias[0][1] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
	elif(lateral == 4):
		if(lavanderias[0][0] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
		elif(lavanderias[1][0] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05) #Virar Esquerda
			x = linha
		elif(lavanderias[1][1] == 1):
			distRodas = 5894
			move_tank.on(SpeedPercent(40), SpeedPercent(40)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha
		elif(lavanderias[0][1] == 1):
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				

			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05) #Virar Direita
			x = 7 - linha

	motorDir.reset()
	move_tank.on(SpeedPercent(40), SpeedPercent(40))

	while(motorDir.position < (x*842 + 200)):
		pass
	move_tank.on(SpeedPercent(0), SpeedPercent(0))
	largaBloco(garra_drive, move_tank)
	return