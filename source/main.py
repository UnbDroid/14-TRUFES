from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from inicializacao import iniciar
from achaCubo import *
from garra import *

N = 824

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
		distancia = ultrassom.value()
		print("LAVANDA:", colorE.value())
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and (distTot - distMot) > 500):
			alinhaTempo(colorE, colorD, 40, move_tank, atualiza)
	move_tank.on(SpeedPercent(0), SpeedPercent(0))
	if(atualiza):
		move_steering = MoveSteering(OUTPUT_C, OUTPUT_D)
		move_steering.on_for_rotations(-30, SpeedPercent(-50), 4)
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

def controla(numCubos):
	comCubo = False
	linha = 1
	lateral = 4
	atualiza = False

	while(numCubos < 4):
		while(comCubo == False):
			descerLateral()
			linha += 1
			comCubo = verificaLinha()

		motorEsq.reset()
		motorDir.reset()
		move_tank.on(SpeedPercent(40), SpeedPercent(40))  # Inicia movimento

		while (ultrassom.value() > 90):
			if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and ultrassom.value() > 310):
				alinhaTempo(colorE, colorD, 40, move_tank, False)
		move_tank.on(SpeedPercent(0), SpeedPercent(0))
		print("HERE1")
		comCubo, atualiza= pegaBloco(move_garra, move_tank, lateral, coresLavanderias, lavanderias, colorF)  # Função de aproximar e pegar o bloco
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
			lateral -= 1
			linha = 2
			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),2.1)
			move_tank.on_for_rotations(SpeedPercent(30), SpeedPercent(-30), 1.05)
			comCubo = verificaLinha()
		elif(comCubo):
			move_tank.on_for_rotations(SpeedPercent(40), SpeedPercent(-40),2.1)
			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(40), SpeedPercent(40))
			while((((linha-1)*N) - distRodas) > 120):
				distRodas = int((motorEsq.position + motorDir.position)/2)
		comCubo = False
			# Voltar a distância andada (baseada no quanto as rodas andaram até o cubo, no valor do ultrassom ou nas linhas passadas no chão)
			# Virar de ré
			# Alinhar com a lateral
			# Andar até a lavanderia
			# Terminar o movimento de acordo com a lateral
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
	else:
		# Só existe uma lavanderia sem cubo
		# chamar função de achar um cubo
		lateral = 0
	return lateral

if __name__ == '__main__':
	garraE, garraD, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias = iniciar()
	move_garra = MoveTank(OUTPUT_A, OUTPUT_B, motor_class=MediumMotor)
	motorEsq = LargeMotor(OUTPUT_C)
	motorDir = LargeMotor(OUTPUT_D)
	lavanderias, disponibilidade = leArquivo() # Pegando informações da matriz disponibilidade
	if disponibilidade[0] == 1 and disponibilidade[1] == 1 and disponibilidade[2] == 1 and disponibilidade[3] == 1:
		controla(0)
	else:
		numCubos = disponibilidade.count(0)
		lateral = lateralDisponivel(lavanderias)
		if lateral == 0:
			#chamar função de procurar um cubo
			print('uhu')
		else:
			#direcionar para a lateral
			controla(numCubos)


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