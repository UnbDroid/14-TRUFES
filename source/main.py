from ev3dev2.motor import *
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import *
from inicializacao import setRobot
from achaCubo import *
from garra import *
from ultimoBloco import ultimoBloco
from support import *

N = 804
VEL = 40
VELROT = 30
STOP = SpeedPercent(0)
ROT90 = 1.03
ROT180 = 2.05
DISTPAREDE = 90

def vaiLavanderia(linha, move_tank, motorEsq, motorDir, atualiza):
	motorEsq.reset()
	motorDir.reset()
	distMot = 0
	distancia = 1000
	if(atualiza):
		#move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), 0.1)
		move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL))
		distTot = (7-linha)*N
	else:
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		distTot = N*(linha-2) + 220
	

	while((distTot - distMot) > 0):
		distMot = abs(int((motorEsq.position + motorDir.position)/2))
		distancia = filterultrassom(ultrassom)
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and (distTot - distMot) > 400):
			alinhaTempo(colorE, colorD, 40, move_tank, atualiza)
	move_tank.on(STOP, STOP)
	if(atualiza):
		drift(True, move_tank, move_steering)
	return

def leArquivo():
	lavanderias = [[1 for i in range(2)] for j in range(2)] # Todas lavanderias iniciam disponíveis
	arq = open('matriz.txt', 'r')
	texto = arq.read().split()
	lavanderias[0][0] = int(texto[0])
	lavanderias[0][1] = int(texto[1])
	lavanderias[1][0] = int(texto[2])
	lavanderias[1][1] = int(texto[3])
	arq.close()
	print(lavanderias)
	return lavanderias, texto


def escreveArquivo():
	arq = open('matriz.txt', 'w')
	arq.write(str(lavanderias[0][0])+" "+str(lavanderias[0][1])+" "+str(lavanderias[1][0])+" "+str(lavanderias[1][1]))
	arq.close()

def ultimoCubo(linha, move_garra, motorDir):
	
	move_garra.on(SpeedPercent(-10), SpeedPercent(10)) # Abre garras continuamente
	move_garra.wait_until_not_moving()
	move_garra.off()

	time.sleep(0.4)
	distDir = motorDir.position
	flag = True

	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
	while((motorDir.position - distDir) < 431):
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and flag):
			
			flag = False
			distDir -= 100
	move_tank.on(STOP, STOP)
	move_garra.on(SpeedPercent(10), SpeedPercent(-10)) # Fecha garras continuamente
	time.sleep(0.1)
	move_garra.wait_until_not_moving()
	move_garra.off()
	ultimoBloco(linha, lavanderias, lateral, move_tank, int((motorEsq.position + motorDir.position)/2), move_garra, motorDir)

def controla(numCubos, lateral):
	comCubo = False
	linha = 1
	atualiza = False
	flag = 1
	while(numCubos < 4):
		while(comCubo == False):
			if lateral == 4 and lavanderias[0][0] == 0 and flag:
				comCubo = verificaLinha(move_tank, ultrassom, colorE, colorD, motorDir, linha)
				flag = 0
				linha = 2
			else:
				descerLateral(move_tank, motorEsq, motorDir, ultrassom, colorE, colorD)
				linha += 1
				
				motorEsq.reset()
				motorDir.reset()
				comCubo = verificaLinha(move_tank, ultrassom, colorE, colorD, motorDir, linha)
			if(linha == 7 and comCubo == False): #Se chegar no final sem pegar o cubo 'atualiza', tem que virar e continuar de qualquer jeito
				
				
				if(lateral == 4 and lavanderias [0][1] == 0):
					drift(False, move_tank, move_steering)
				elif(lateral == 3 and lavanderias [1][1] == 0):
					drift(False, move_tank, move_steering)
				elif(lateral == 2 and lavanderias [1][0] == 0):
					drift(False, move_tank, move_steering)
				elif(lateral == 1 and lavanderias [0][0] == 0):
					drift(False, move_tank, move_steering)
				else:
					
					move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
					drift(True, move_tank, move_steering)
				atualiza = True
				break
			

		if(atualiza == False):
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))  # Inicia movimento
			ultraDist = filterultrassom(ultrassom)
			while (ultraDist > 120):
				ultraDist = filterultrassom(ultrassom)
				
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and filterultrassom(ultrassom) > 310):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			move_tank.on(STOP, STOP)
			
			if(numCubos < 3):
				comCubo, atualiza= pegaBloco(move_garra, move_tank, lateral, coresLavanderias, lavanderias, colorF, colorE, colorD)  # Função de aproximar e pegar o bloco
			else:
				ultimoCubo(linha, move_garra, motorDir)
			#::Podemos fazer ele seguir colado na parede para ter mais espaço para virar no fim da arena
			distRodas = int((motorEsq.position + motorDir.position)/2)

			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			distRe = 0
			
			while(distRodas - (distRe) > 60):
				distRe =  abs(int((motorEsq.position + motorDir.position)/2))
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and distRodas - (distRe) > 500):
					alinhaTempo(colorE, colorD, 40, move_tank, True)

			if(comCubo):
				move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT),ROT90)
				vaiLavanderia(linha, move_tank, motorEsq, motorDir, atualiza)
				numCubos += 1
				largaBloco(move_garra, move_tank)
				escreveArquivo()
			else:
				move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)


		if(atualiza):
			lateral = lateral - 1 if (lateral != 1) else 4
			linha = 2
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT180)
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
			comCubo = verificaLinha(move_tank, ultrassom, colorE, colorD, motorDir, linha)
			atualiza = False
		elif(comCubo):
			move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT180)
			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
			while((((linha-2)*N) - distRodas) > 10):
				distRodas = int((motorEsq.position + motorDir.position)/2)
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and filterultrassom(ultrassom) > 310):
					alinhaTempo(colorE, colorD, 40, move_tank, False)
			comCubo = False
			linha -= 1
	return

if __name__ == '__main__':
	motorEsq = LargeMotor(OUTPUT_C)
	motorDir = LargeMotor(OUTPUT_D)
	btn = Button()
	sound = Sound()
	lavanderias, disponibilidade = leArquivo() # Pegando informações da matriz disponibilidade
	lateral = 0

	while not btn.any(): # Espera o botão
		time.sleep(0.01)

	sound.beep() #Beeep
	
	move_steering = MoveSteering(OUTPUT_C, OUTPUT_D)
	move_garra, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias, lateral, numCubos, move_steering = setRobot(lavanderias, disponibilidade)
	controla(numCubos, lateral)

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