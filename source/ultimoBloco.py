from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from garra import *
from alinhamentoTempo import alinhaTempo

# Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

#Define Vars
N = 780
VEL = 40
STOP = SpeedPercent(0)
ROT90 = 1.03
ROT180 = 2.05

def ultimoBloco(linha, lavanderias, lateral, move_tank, distRodas, garra_drive, motorDir, colorE, colorD, y):
	"Pega o ultimo bloco ignorando o resto dos comandos para levar para a ultima lavanderia desocupada"
	motorDir.reset()

	y = int((y*360)/150)

	# Inicia quando já está com o cubo preso na garra
	# Baseado na lateral atual do robô
	# Depois de verificar qual lavanderia está livre, se movimenta até ela pelo meio da arena.
	if(lateral == 1): 
		if(lavanderias[0][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][1] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[0][1] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
	elif(lateral == 2):
		if(lavanderias[0][0] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[0][1] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
	elif(lateral == 3):
		if(lavanderias[0][0] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][0] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[1][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[0][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
	elif(lateral == 4):
		if(lavanderias[0][0] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][0] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
			x = linha
		elif(lavanderias[1][1] == 1):
			distRodas = y
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) # Avançando
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha
		elif(lavanderias[0][1] == 1):
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			while(distRodas - abs(motorDir.position) > 0):
				if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
					# Alinhamento
					alinhaTempo(colorE, colorD, VEL, move_tank, True)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			x = 7 - linha

	motorDir.reset()
	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL)) #Vai até a lavanderia

	while(motorDir.position < (x*N + 200)):
		#Enquanto, a partir da linha que se encontrava o robô, não chega na lavanderia, avança.
		if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK and motorDir.position < (x*N - 200)):
			# Alinhamento
			alinhaTempo(colorE, colorD, VEL, move_tank, False)
	move_tank.on(STOP, STOP)
	largaBloco(garra_drive, move_tank)
	#Acabou. 
	return



def victoryLap(move_tank, colorE, colorD, ultrassom):
	linha = 2
	count = 0

	move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 1)
	move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL), ROT90)
	if(ultrassom.value() < 400):
		move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL), ROT180)
		move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 2.2)
		move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL), ROT90)
	move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 2.8)
	move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(VEL),ROT90) #Virar Esquerda
	move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 0.7)

	#colorE.calibrate_white()
	#colorD.calibrate_white()

	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
	while(count < 4):
		if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
			# Alinhamento
			alinhaTempo(colorE, colorD, VEL, move_tank, False)
			linha += 1
		if(linha == 7):
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 0.7)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 4.5)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 1.7)
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(-VEL),ROT90) #Virar Direita
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 2.6)
			move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 2.05) # 180º esquerda
			move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 0.7)
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
			linha = 2
			count += 1


if __name__ == '__main__':
	move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
	colorE = ColorSensor(INPUT_3)
	colorD = ColorSensor(INPUT_4)

	colorE.mode = 'COL-COLOR'
	colorD.mode = 'COL-COLOR'

	victoryLap(move_tank, colorE, colorD)
