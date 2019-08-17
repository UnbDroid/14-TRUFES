from ev3dev2.motor import *
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import *
from inicializacao import iniciar
from achaCubo import *
from garra import *
from ultimoBloco import ultimoBloco

N = 824

def filterultrassom(ultrassom):
	valor = 0
	for i in range(0, 10):
		valor += ultrassom.value()
	return int(valor/10)

def drift(super)
	#Se super for True, o robô vai dar drift de ré.
	#Se não, ele faz a volta na lavanderia
	move_steering = MoveSteering(OUTPUT_C, OUTPUT_D)
	move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
	if(super):
		move_steering.on_for_rotations(-22, SpeedPercent(-50), 4.55)
	else:
		move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2.252)
		move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.05)
		move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2.252)
		move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)

def vaiLavanderia(linha, move_tank, motorEsq, motorDir, atualiza):
	motorEsq.reset()
	motorDir.reset()
	distMot = 0
	distancia = 1000
	if(atualiza):
		move_tank.on(SpeedPercent(-40), SpeedPercent(-40))
		distTot = (7-linha)*N
	else:
		move_tank.on(SpeedPercent(40), SpeedPercent(40))
		distTot = N*(linha-2) + 220
	print('linha:', linha, 'dist:', distTot)

	while((distTot - distMot) > 0):
		distMot = abs(int((motorEsq.position + motorDir.position)/2))
		distancia = filterultrassom(ultrassom)
		print("LAVANDA:", colorE.value())
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and (distTot - distMot) > 500):
			alinhaTempo(colorE, colorD, 40, move_tank, atualiza)
	move_tank.on(SpeedPercent(0), SpeedPercent(0))
	if(atualiza):
		drift()
	return

def leArquivo():
	lavanderias = [[1 for i in range(2)] for j in range(2)] # Todas lavanderias iniciam disponíveis
	arq = open('matriz.txt', 'r')
	texto = arq.read().split()
	lavanderias[0][0] = int(texto[0])
	lavanderias[0][1] = int(texto[1])
	lavanderias[1][0] = int(texto[2])
	lavanderias[1][1] = int(texto[1])
	arq.close()
	print(lavanderias)
	return lavanderias, texto


def escreveArquivo():
	arq = open('matriz.txt', 'w')
	arq.write(str(lavanderias[0][0])+" "+str(lavanderias[0][1])+" "+str(lavanderias[1][0])+" "+str(lavanderias[1][1]))
	arq.close()

def ultimoCubo(linha):
	garra1 = MediumMotor(OUTPUT_A)
	garra2 = MediumMotor(OUTPUT_B)
	move_garra.on(SpeedPercent(10), SpeedPercent(-10)) # Abre garras continuamente
	garra_drive.wait_until_not_moving()
	garra_drive.off()

	time.sleep(0.4)
	distDir = motorDir.position
	flag = True

	tank_drive.on(SpeedPercent(40), SpeedPercent(40))
	while((motorDir.position - distDir) < 431):
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and flag):
			print("Heh")
			flag = False
			distDir -= 100
	tank_drive.on(SpeedPercent(0), SpeedPercent(0))
	garra_drive.on(SpeedPercent(-10), SpeedPercent(10)) # Fecha garras continuamente
	time.sleep(0.1)
	garra_drive.wait_until_not_moving()
	garra_drive.off()
	ultimoBloco(linha, lavanderias, lateral, move_tank, int((motorEsq.position + motorDir.position)/2), move_garra)

def controla():
	comCubo = False
	numCubos = 0
	linha = 1
	atualiza = False

	while(numCubos < 4):
		while(comCubo == False):
			descerLateral()
			linha += 1
			if(linha > 6): #Se chegar no final sem pegar o cubo 'atualiza', tem que virar e continuar de qualquer jeito
				if(lateral == 4 and lavanderias [0][1] == 0):
					drift(False)
				elif(lavanderia == 3 and lavanderias [1][1] == 0):
					drift(False)
				elif(lavanderia == 2 and lavanderias [1][0] == 0):
					drift(False)
				elif(lavanderia == 1 and lavanderias [0][0] == 0):
					drift(False)					
				else: 
					drift(True)
				atualiza = True
				break
			comCubo = verificaLinha()

		if(atualiza == False):
			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(40), SpeedPercent(40))  # Inicia movimento

			while (filterultrassom(ultrassom) > 90):
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and filterultrassom(ultrassom) > 310):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			move_tank.on(SpeedPercent(0), SpeedPercent(0))
			print("HERE1")
			if(numCubos == 3):
				comCubo, atualiza= pegaBloco(move_garra, move_tank, lateral, coresLavanderias, lavanderias, colorF)  # Função de aproximar e pegar o bloco
			else:
				ultimoCubo(linha)
			#::Podemos fazer ele seguir colado na parede para ter mais espaço para virar no fim da arena
			distRodas = int((motorEsq.position + motorDir.position)/2)

			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(-40), SpeedPercent(-40)) # Dando ré
			distRe = 0
			print('Tot:', distRodas)
			while(distRodas - (distRe) > 0):
				distRe =  abs(int((motorEsq.position + motorDir.position)/2))
				print('Re', distRe)

			if(comCubo):
				move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),1.05)
				vaiLavanderia(linha, move_tank, motorEsq, motorDir, atualiza)
				numCubos += 1
				largaBloco(move_garra, move_tank)
				escreveArquivo()
			else:
				move_tank.on_for_rotations(SpeedPercent(-40), SpeedPercent(40),1.05)


		if(atualiza):
			lateral = lateral - 1 if (lateral != 1) else 4
			linha = 2
			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),2.1)
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)
			comCubo = verificaLinha()
			atualiza = False
		elif(comCubo):
			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),2.1)
			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while((((linha-1)*N) - distRodas) > 120):
				distRodas = int((motorEsq.position + motorDir.position)/2)
		comCubo = False
	return

def lateralDisponivel(lavanderias):
	if lavanderias[0][0] == 1 and lavanderias[1][0] == 1:
		lateral = 1
	elif lavanderias[1][0] == 1 and lavanderias[1][1] == 1:
		lateral = 2
	elif lavanderias[1][1] == 1 and lavanderias[0][1] == 1:
		lateral = 3
	elif lavanderias[0][1] == 1 and lavanderias[0][0] == 1:
		lateral = 4
	elif lavanderias[0][0] == 1 and lavanderias[1][1] == 1:
		lateral = 5
	elif lavanderias[1][0] == 1 and lavanderias[0][1] == 1:
		lateral = 5
	else:
		# Só existe uma lavanderia sem cubo
		# chamar função de achar um cubo
		lateral = 0
	return lateral

def gogo(disponibilidade, lateral):
	if disponibilidade[0] == 1 and disponibilidade[1] == 1 and disponibilidade[2] == 1 and disponibilidade[3] == 1:
		lateral = 4
		controla(0)
	else:
		if lateral == 0:
			# uma lavanderia sem cubo
			print('falta fazer')
		elif lateral == 1:
			# 180º
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 2.10)
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while (filterultrassom(ultrassom)) >= 90:
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			move_tank.on(SpeedPercent(0), SpeedPercent(0))
			# para na lavanderia da lavanderia 1 e vira para iniciar
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 2.10)

		elif lateral == 2:
			# 180º
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 2.10)
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while (filterultrassom(ultrassom)) >= 90:
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			move_tank.on(SpeedPercent(0), SpeedPercent(0))
			# chegou na lavanderia da lateral 2 (90º)
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)
			
			# subindo a lateral
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while (filterultrassom(ultrassom)) >= 90:
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			move_tank.on(SpeedPercent(0), SpeedPercent(0))
			# 180ºcv f hmjklmyjrvwt (ass: Bianca)
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 2.10)
		
		elif lateral == 3:
			contLinha = 0
			move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.05)
			# segue reto
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while contLinha < 7:
				if (filterultrassom(ultrassom)) <= 90:
					#contornar
					move_tank.on(SpeedPercent(0), SpeedPercent(0))
					move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.05)
					move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 2.252)
					move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)
					move_tank.on(SpeedPercent(40), SpeedPercent(40))
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
					contLinha += 1
			# chegamos na lateral 3
			move_tank.on(SpeedPercent(0), SpeedPercent(0))
			move_tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 0.1)
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)
			# direcionando para a lavanderia
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while (filterultrassom(ultrassom)) >= 90:
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			move_tank.on(SpeedPercent(0), SpeedPercent(0))
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 2.10)

		elif lateral == 4:
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while (filterultrassom(ultrassom)) >= 90:
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			move_tank.on(SpeedPercent(0), SpeedPercent(0))
			# chegou na lavanderia da lateral 4 (90º)
			move_tank.on_for_rotations(SpeedPercent(-30), SpeedPercent(30), 1.05)
		elif lateral == 5:
			# diagonal ocupada
			print('falta fazer')			
		
		# após chegar na lateral reinicia suas funcionalidades
		numCubos = disponibilidade.count(0)
		controla(numCubos)

if __name__ == '__main__':
	garraE, garraD, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias = iniciar()
	move_garra = MoveTank(OUTPUT_A, OUTPUT_B, motor_class=MediumMotor)
	motorEsq = LargeMotor(OUTPUT_C)
	motorDir = LargeMotor(OUTPUT_D)
	btn = Button()
	sound = Sound()
	lavanderias, disponibilidade = leArquivo() # Pegando informações da matriz disponibilidade

	while not btn.any(): # Espera o botão
    	time.sleep(0.01)

	sound.beep() #Beeep
	
	lateral = lateralDisponivel(lavanderias)
	gogo(disponibilidade, lateral)

# Após iniciar teremos uma matriz de cores das lavanderias (coresLavanderias que é uma matriz 2x2) na qual inicialmente
# estão pretas. A disponibilidadeLavanderias (matriz 2x2) é iniciada com todas lavanderias disponíveis (True/1)

# Lateral é uma "flag" para podermos nos localizar e fazer a verificação das matrizes de cor e disponibilidade

# Começará na lateral 4 e percorrerá em ordem decrescente

# Lateral = 1 significa as posições [0][0] e [1][0]
# Lateral = 2 significa as posições [1][0] e [1][1]
# Lateral = 3 significa as posições [1][1] e [0][1]
# Lateral = 4 significa as posições [0][1] e [0][0]

# Desenvolver e inserir código que percorre a arena verificando se existe cubo nas linhas, utilizando a matriz de cores
# que já foi inicializada na iniciar() sendo que o robô deve começar virado pra esquerda e a lavanderia [0][0] é a 
# a superior esquerda. 
# A lógica de pegar ou não um cubo com base na matriz de cores e disponibilidade já está desenvolvida na pegaBloco()
# Mais especificamente na verificaBloco()