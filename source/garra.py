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
Livre = 1
Ocupada = 0

N = 804

def verificaBloco(lateral, coresLavanderias, lavanderias, sensorFrontal):
	# Filtro de verificação da cor do cubo
	cont = 0
	corBloco = 0
	Atualiza = False
	while cont < 5:
		corBloco += sensorFrontal.value()
		print(corBloco)
		cont +=1
	print('Cor: ', corBloco)
	corBloco = Preto if (int(corBloco/5) < 15) else Branco
	print('Cor final: ', corBloco)
	##########################################

	if lateral == 1:
		if coresLavanderias[0][0] == corBloco:
			if lavanderias[0][0] == Livre:
				lavanderias[0][0] = Ocupada
				Atualiza = True
				return True, Atualiza
			else:
				return False, Atualiza
		else:
			if lavanderias[1][0] == Livre:
				lavanderias[1][0] = Ocupada
				return True, Atualiza
			else:
				return False, Atualiza
		
	elif lateral == 2:
		if coresLavanderias[1][0] == corBloco:
			if lavanderias[1][0] == Livre:
				lavanderias[1][0] = Ocupada
				Atualiza = True
				return True, Atualiza
			else:
				return False, Atualiza
		else:
			if lavanderias[1][1] == Livre:
				lavanderias[1][1] = Ocupada
				return True, Atualiza
			else:
				return False, Atualiza
	elif lateral == 3:
		if coresLavanderias[1][1] == corBloco:
			if lavanderias[1][1] == Livre:
				lavanderias[1][1] = Ocupada
				Atualiza = True
				return True, Atualiza
			else:
				return False, Atualiza
		else:
			if lavanderias[0][1] == Livre:
				lavanderias[0][1] = Ocupada
				return True, Atualiza
			else:
				return False, Atualiza
	elif lateral == 4: 
		if coresLavanderias[0][1] == corBloco:
			if lavanderias[0][1] == Livre:
				lavanderias[0][1] = Ocupada
				Atualiza = True
				return True, Atualiza
			else:
				return False, Atualiza
		else:
			if lavanderias[0][0] == Livre:
				lavanderias[0][0] = Ocupada
				return True, Atualiza
			else:
				return False, Atualiza

def pegaBloco(garra_drive, tank_drive, lateral, coresLavanderias, lavanderias, sensorFrontal, colorE, colorD):
	garra1 = MediumMotor(OUTPUT_A)
	garra2 = MediumMotor(OUTPUT_B)
	motorDir = LargeMotor(OUTPUT_D)

	garra_drive.on(SpeedPercent(-10), SpeedPercent(10)) # Abre garras continuamente
	time.sleep(0.1)
	garra_drive.wait_until_not_moving()
	garra_drive.off()

	distDir = motorDir.position
	flag = True

	tank_drive.on(SpeedPercent(40), SpeedPercent(40))
	while((motorDir.position - distDir) < 360):
		print("Heh:", distDir)
		print("He:", motorDir.position)
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and flag):
			flag = False
			distDir -= 100
	distDir = motorDir.position
	tank_drive.on(SpeedPercent(-10), SpeedPercent(-10))	
	while((motorDir.position - distDir) < 15):
		pass
	tank_drive.on(SpeedPercent(0), SpeedPercent(0))
	verifica, Atualiza = verificaBloco(lateral, coresLavanderias, lavanderias, sensorFrontal)
	if(verifica):
		garra_drive.on(SpeedPercent(10), SpeedPercent(-10)) # Fecha garras continuamente
		time.sleep(0.1)
		garra_drive.wait_until_not_moving()
		garra_drive.off()
		return True, Atualiza
	# Se não tiver que pegar, se afasta para deixar
	else:
		tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(-40), 0.7) 
		garra_drive.on_for_rotations(SpeedPercent(10), SpeedPercent(-10), 0.32) # Fecha garras
		garra_drive.off()
		garra1.reset()
		garra2.reset()
		return False, Atualiza

def largaBloco(garra_drive, tank_drive):
	garra1 = MediumMotor(OUTPUT_A)
	garra2 = MediumMotor(OUTPUT_B)
	garra_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(10), 0.25) # Abre garras
	tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(-40), 0.7) # Ré com base em 125mm de distância do cubo
	garra_drive.on_for_rotations(SpeedPercent(10), SpeedPercent(-10), 0.35) # Fecha garras
	garra_drive.off()
	garra1.reset()
	garra2.reset()

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



