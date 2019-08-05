from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from time import sleep

#Definindo o nome das cores da matriz de cores
Preto = 0
Branco = 1

#Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

#Disponibilidade
Livre = True
Ocupada = False

def verificaBloco(lateral, coresLavanderias, lavanderias, sensorFrontal):
	# Filtro de verificação da cor do cubo
	cont = 0
	cor = 0
	while cont < 5:
		cor += sensorFrontal.value()
		cont +=1
	cor = int(cor/5)
	##########################################
	
	if(cor < 11):
		print("Preto: ", cor)
		if lateral == 1: #[0][0] e [1][0]
			if coresLavanderias[0][0] == Preto:
				if lavanderias[0][0] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[1][0] == Preto
				if lavanderias[1][0] == Livre:
					return True
				else:
					return False
			
		elif lateral == 2:
			if coresLavanderias[1][0] == Preto:
				if lavanderias[1][0] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[1][1] == Preto
				if lavanderias[1][1] == Livre:
					return True
				else:
					return False
		elif lateral == 3:
			if coresLavanderias[1][1] == Preto:
				if lavanderias[1][1] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[0][1] == Preto
				if lavanderias[0][1] == Livre:
					return True
				else:
					return False
		elif lateral == 4: 
			if coresLavanderias[0][1] == Preto:
				if lavanderias[0][1] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[0][0] == Preto
				if lavanderias[0][0] == Livre:
					return True
				else:
					return False
	elif(cor >= 11):
		print("Branco: ", cor)
		if lateral == 1: #[0][0] e [1][0]
			if coresLavanderias[0][0] == Branco:
				if lavanderias[0][0] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[1][0] == Branco
				if lavanderias[1][0] == Livre:
					return True
				else:
					return False
			
		elif lateral == 2:
			if coresLavanderias[1][0] == Branco:
				if lavanderias[1][0] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[1][1] == Branco
				if lavanderias[1][1] == Livre:
					return True
				else:
					return False
		elif lateral == 3:
			if coresLavanderias[1][1] == Branco:
				if lavanderias[1][1] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[0][1] == Branco
				if lavanderias[0][1] == Livre:
					return True
				else:
					return False
		elif lateral == 4: 
			if coresLavanderias[0][1] == Branco:
				if lavanderias[0][1] == Livre:
					return True
				else:
					return False
			else: 
				# coresLavanderias[0][0] == Branco
				if lavanderias[0][0] == Livre:
					return True
				else:
					return False
	else:
		print(cor)

def pegaBloco(garra1, garra2, tank_drive,lateral, coresLavanderias, lavanderias, sensorFrontal):
	garra1.on_for_rotations(SpeedPercent(10), 0.25) #garra da esquerda abre
	garra2.on_for_rotations(SpeedPercent(-10), 0.25) #garra da direita abre
	tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 0.7) #movimenta com base em 125mm de distância do cubo
	sleep(0.5)
	if(verificaBloco(lateral, coresLavanderias, lavanderias, sensorFrontal)):
		garra1.on_for_rotations(SpeedPercent(-10), 0.125) #garra da esquerda fecha
		garra2.on_for_rotations(SpeedPercent(10), 0.125) #garra da direita fecha
		garra1.on_for_rotations(SpeedPercent(-10), 0.125) #garra da esquerda fecha
		garra2.on_for_rotations(SpeedPercent(10), 0.125) #garra da direita fecha
	# Se não tiver que pegar, se afasta para deixar
	else:
		tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(-40), 0.7) 
		garra1.on_for_rotations(SpeedPercent(-10), 0.25) #garra da esquerda fecha
		garra2.on_for_rotations(SpeedPercent(10), 0.25) #garra da direita fecha

def largaBloco(garra1, garra2, tank_drive):
	garra1.on_for_rotations(SpeedPercent(10), 0.05) #garra da esquerda abre
	garra2.on_for_rotations(SpeedPercent(-10), 0.05) #garra da direita abre
	garra1.on_for_rotations(SpeedPercent(10), 0.2) #garra da esquerda abre
	garra2.on_for_rotations(SpeedPercent(-10), 0.2) #garra da direita abre
	tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(-40), 0.7) #ré com base em 125mm de distância do cubo
	garra1.on_for_rotations(SpeedPercent(-10), 0.25) #garra da esquerda fecha
	garra2.on_for_rotations(SpeedPercent(10), 0.25) #garra da direita fecha

if __name__ == '__main__':

	lateral = 1 # Pode ser de 1 a 4, sendo que significa em qual lateral estamos com base na posição
	# Lateral = 1 significa as posições [0][0] e [1][0]
	# Lateral = 2 significa as posições [1][0] e [1][1]
	# Lateral = 3 significa as posições [1][1] e [0][1]
	# Lateral = 4 significa as posições [0][1] e [0][0]

	lavanderias = [[1 for i in range(2)] for j in range(2)] # Todas lavanderias estão livres
	coresLavanderias = [[Preto for i in range(2)] for j in range(2)] # Todas lavanderias são pretas

	lavanderias[0][0] = False

	# Lavandeira exemplo #
	coresLavanderias[0][0] = Preto
	coresLavanderias[0][1] = Branco
	coresLavanderias[1][0] = Branco
	coresLavanderias[1][1] = Preto
	######################

	tank_drive = MoveTank(OUTPUT_C, OUTPUT_D)  
	ultrassom = UltrasonicSensor(INPUT_1)
	garra1 = Motor(OUTPUT_A)
	garra2 = Motor(OUTPUT_B)
	# Sem aplicar modo no leitor frontal
	sensorFrontal = ColorSensor(INPUT_2)
	
	tank_drive.on(SpeedRPM(40), SpeedRPM(40)) #inicia movimento
	while(ultrassom.value() > 130):
		g=1
	tank_drive.on(SpeedRPM(0), SpeedRPM(0)) #para movimento
	pegaBloco(garra1, garra2, tank_drive, lateral, coresLavanderias, lavanderias, sensorFrontal) #função de aproximar e pegar o bloco
	tank_drive.on_for_rotations(SpeedPercent(-50),SpeedPercent(-50), 2) # 360 para teste
	largaBloco(garra1, garra2, tank_drive) #função que afasta e larga o bloco



