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
Ativa = 2
Livre = 1
Ocupada = 0
Atualiza = False

def verificaBloco(lateral, coresLavanderias, lavanderias, sensorFrontal):
	# Filtro de verificação da cor do cubo
	cont = 0
	corBloco = 0
	while cont < 5:
		corBloco += sensorFrontal.value()
		cont +=1
	corBloco = Preto if (int(corBloco/5) < 11) else Branco
	##########################################

	if lateral == 1:
		if coresLavanderias[0][0] == corBloco:
			if lavanderias[0][0] == Livre:
				lavanderias[0][0] = Ativa
				return True
			else:
				return False
		else:
			if lavanderias[1][0] == Livre:
				lavanderias[1][0] = Ativa
				Atualiza = True
				return True
			else:
				return False
		
	elif lateral == 2:
		if coresLavanderias[1][0] == corBloco:
			if lavanderias[1][0] == Livre:
				lavanderias[1][0] = Ativa
				return True
			else:
				return False
		else:
			if lavanderias[1][1] == Livre:
				lavanderias[1][1] = Ativa
				Atualiza = True
				return True
			else:
				return False
	elif lateral == 3:
		if coresLavanderias[1][1] == corBloco:
			if lavanderias[1][1] == Livre:
				lavanderias[1][1] = Ativa
				return True
			else:
				return False
		else:
			if lavanderias[0][1] == Livre:
				lavanderias[0][1] = Ativa
				Atualiza = True
				return True
			else:
				return False
	elif lateral == 4: 
		if coresLavanderias[0][1] == corBloco:
			if lavanderias[0][1] == Livre:
				lavanderias[0][1] = Ativa
				return True
			else:
				return False
		else:
			if lavanderias[0][0] == Livre:
				lavanderias[0][0] = Ativa
				Atualiza = True
				return True
			else:
				return False

def pegaBloco(garra_drive, tank_drive,lateral, coresLavanderias, lavanderias, sensorFrontal):
	garra_drive.on_for_rotations(SpeedPercent(10), SpeedPercent(-10), 0.25) # Abre as garras
	tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 0.7) # Movimenta com base em 125mm de distância do cubo
	sleep(0.5)
	if(verificaBloco(lateral, coresLavanderias, lavanderias, sensorFrontal)):
		garra_drive.on(SpeedPercent(-10), SpeedPercent(10)) # Fecha garras continuamente
		garra_drive.wait_until_not_moving()
		garra_drive.off()
		return True, Atualiza
	# Se não tiver que pegar, se afasta para deixar
	else:
		tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(-40), 0.7) 
		garra_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(10), 0.25) # Fecha garras
		return False, Atualiza

def largaBloco(garra_drive, tank_drive):
	garra_drive.on_for_rotations(SpeedPercent(10), SpeedPercent(-10), 0.25) # Abre garras
	tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(-40), 0.7) # Ré com base em 125mm de distância do cubo
	garra_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(10), 0.25) # Fecha garras

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
	move_garra = MoveTank(OUTPUT_A, OUTPUT_B, motor_class=MediumMotor)
	# Sem aplicar modo no leitor frontal
	sensorFrontal = ColorSensor(INPUT_2)
	
	tank_drive.on(SpeedRPM(40), SpeedRPM(40)) # Inicia movimento
	while(ultrassom.value() > 130):
		g=1
	tank_drive.on(SpeedRPM(0), SpeedRPM(0)) # Para movimento
	pegaBloco(move_garra, tank_drive, lateral, coresLavanderias, lavanderias, sensorFrontal) # Função de aproximar e pegar o bloco
	tank_drive.on_for_rotations(SpeedPercent(-50),SpeedPercent(-50), 2) # 360 para teste
	largaBloco(move_garra, tank_drive) # Função que afasta e larga o bloco



