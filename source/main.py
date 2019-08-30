from ev3dev2.motor import *
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import *
from inicializacao import setRobot
from achaCubo import *
from garra import *
from ultimoBloco import ultimoBloco, victoryLap
from support import *

# Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

N = 780
VEL = 45
VELROT = 30
STOP = SpeedPercent(0)
ROT90 = 1.03
ROT180 = 2.05
DISTPAREDE = 90

def vaiLavanderia(linha, move_tank, motorEsq, motorDir, atualiza):
	motorEsq.reset()
	motorDir.reset()
	distMot = 0

	if(atualiza):
		# Vai até a lavanderia da próxima lateral
		move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL))
		distTot = (7-linha)*N + 80 # Distancia a ser andada, pela linha atual até a última linha
	else:
		# Vai até a lavanderia de início da lateral
		move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
		distTot = N*(linha-2) + 240 # Distancia a ser andada, pela linha atual até o começo
	

	while((distTot - distMot) > 0):
		distMot = abs(int((motorEsq.position + motorDir.position)/2)) # Média entre as distâncias andadas por cada motor
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and (distTot - distMot) > 400):
			# Alinha
			alinhaTempo(colorE, colorD, VEL, move_tank, atualiza)
	move_tank.on(STOP, STOP)
	if(atualiza):
		drift(True, move_tank, move_steering) # Super drift
	return

#def leArquivo():
	#lavanderias = [[1 for i in range(2)] for j in range(2)] # Todas lavanderias iniciam disponíveis
	# Lê uma linha com 4 inteiros e coloca na matriz de disponibilidade
	# 1 é livre e 0 é ocupado
	# arq = open('matriz.txt', 'r')
	# texto = arq.read().split()
	# lavanderias[0][0] = int(texto[0])
	# lavanderias[0][1] = int(texto[1])
	# lavanderias[1][0] = int(texto[2])
	# lavanderias[1][1] = int(texto[3])
	# arq.close()
	#print(lavanderias)
	# Retorna uma matriz com a relação da disponibilidade das lavanderias na arena
	#return lavanderias, texto


 #def escreveArquivo(lavanderias):
 	#arq = open('matriz.txt', 'w')
 	#arq.write(str(lavanderias[0][0])+" "+str(lavanderias[0][1])+" "+str(lavanderias[1][0])+" "+str(lavanderias[1][1]))
 	# Atualiza a matriz disponibilidade

 	#arq.close()

def ultimoCubo(linha, move_garra, motorDir, lateral, y, move_tank, colorE, colorD, ultrassom):
	
	move_garra.on(SpeedPercent(-10), SpeedPercent(10)) # Abre garras continuamente
	move_garra.wait_until_not_moving()
	move_garra.off()

	time.sleep(0.4)
	distDir = motorDir.position
	flag = True

	move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))

	# Anda até chegar no cubo
	while((motorDir.position - distDir) < 360):
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and flag):		
			flag = False
			distDir -= 100 # Se entrar no quadrado, andar menos
	move_tank.on(STOP, STOP)
	move_garra.on(SpeedPercent(10), SpeedPercent(-10)) # Fecha garras continuamente
	time.sleep(0.1)
	move_garra.wait_until_not_moving()
	move_garra.off()
	# Chama a função para deixar o último bloco
	move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 1.6)
	ultraValor = filterultrassom(ultrassom)
	print(ultraValor)
	if(ultraValor > 60):
		return
	ultimoBloco(linha, lavanderias, lateral, move_tank, int((motorEsq.position + motorDir.position)/2), move_garra, motorDir, colorE, colorD, y)
	victoryLap(move_tank, colorE, colorD, ultrassom)
	numCubos += 1
	return

def controla(numCubos, lateral):
	comCubo = False # Inicia sem cubo
	linha = 1 # As linha são numeradas de 1 a 8
	atualiza = False
	flag = 1 # Controle da situação de reinicialização
	flagDrift = 0
	vaiNaLoca = False

	while(numCubos < 4):
		while(comCubo == False):
			if(lateral == 4 and lavanderias[0][0] == 0 and flag):
				comCubo = verificaLinha(move_tank, ultrassom, colorE, colorD, motorEsq, motorDir, linha)
				flag = 0
				linha = 2
			elif(linha != 7):
				descerLateral(move_tank, motorEsq, motorDir, ultrassom, colorE, colorD, linha)
				linha += 1
				flag = 0
				motorEsq.reset()
				motorDir.reset()
				comCubo = verificaLinha(move_tank, ultrassom, colorE, colorD, motorEsq, motorDir, linha) # Verifica se existe cubo na linha
			if(linha == 7 and comCubo == False): # Se chegar no final sem pegar o cubo 'atualiza', tem que virar e continuar de qualquer jeito
				# Verifica se é necessário desviar de um cubo na lavanderia
				flagDrift = 1
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
					flagDrift = 0
				atualiza = True # Mudou de lateral
				break
		print(lavanderias)
			
		# Se não mudou de lateral no fim do movimento:
		if(atualiza == False):
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))  # Inicia movimento
			ultraDist = filterultrassom(ultrassom)
			savedUltra = ultraDist
			print("ultraDist", ultraDist)
			while (ultraDist > 210):
				ultraDist = filterultrassom(ultrassom)
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and filterultrassom(ultrassom) > 310):
					# Alinha
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			move_tank.on(STOP, STOP)
			
			if(numCubos < 3):
				comCubo, atualiza= pegaBloco(move_garra, move_tank, lateral, coresLavanderias, lavanderias, colorF, colorE, colorD, ultrassom)  # Função de aproximar e pegar o bloco
			else:
				# Vai pra configuração final
				print("lateral: ", lateral)
				ultimoCubo(linha, move_garra, motorDir, lateral, (2200 - ultraDist), move_tank, colorE, colorD, ultrassom)
				if(numCubos == 4):
					break
			distRodas = int((motorEsq.position + motorDir.position)/2)
			print("distRodas: ", distRodas)	
			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(-VEL), SpeedPercent(-VEL)) # Dando ré
			distRe = 0
			distAndar = 160
			print("LINHA:  ", linha)
			if(linha == 2 and comCubo == True):
				distAndar = 2000 if (savedUltra < 140) else 560

			recupera = 1
			while(abs(distRodas - distRe) > distAndar):
				# Da ré até chegar na parede de novo
				ultraDist = filterultrassom(ultrassom)
				if((ultraDist > 200 or (ultraDist < 2300 and ultraDist > 1700)) and recupera == 1 and comCubo == True):
					#Perdeu o cubo.
					print("ASASAS")
					comCubo = False
					if(atualiza == True):
						recupera = 0
						atualiza = False
					else:
						recupera = 2
					print(numCubos)
				distRe =  abs(int((motorEsq.position + motorDir.position)/2))
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK)):
					# Alinha
					if (abs(distRodas - (distRe)) > 300):
						alinhaTempo(colorE, colorD, VEL, move_tank, True)
					else:
						break
			print(numCubos)
			if(recupera == 0 or recupera == 2):
				# Verifica se é necessário desviar de um cubo na lavanderia
				if(recupera == 0):
					if lateral == 1:
						lavanderias[0][0] = 1
					elif lateral == 2:
						lavanderias[1][0] = 1
					elif lateral == 3:
						lavanderias[1][1] = 1
					elif lateral == 4: 
						lavanderias[0][1] = 1
				else:
					if lateral == 1:
						lavanderias[1][0] = 1
					elif lateral == 2:
						lavanderias[1][1] = 1
					elif lateral == 3:
						lavanderias[0][1] = 1
					elif lateral == 4: 
						lavanderias[0][0] = 1
				flagDrift = 1
				if(linha == 7):
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
						flagDrift = 0
					atualiza = True # Mudou de lateral
			if(linha != 2 and (recupera != 0 and recupera != 2)):
				move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 0.7) # Dando ré


			if(comCubo):
				# Se estiver com cubo, tem que levar até uma lavanderia
				if(linha != 2):
					move_tank.on_for_rotations(SpeedPercent(VEL/2),SpeedPercent(VEL/2), 0.4)
					move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT90)
					# A lavanderia destino é definida pela variável 'atualiza'
					#escreveArquivo() # Atualiza a matriz de disponibilidade
				else:
					move_steering.on_for_rotations(35, SpeedPercent(-VEL), 3.3)
					linha = 3
				print("Esta linha:", linha)
				vaiLavanderia(linha, move_tank, motorEsq, motorDir, atualiza)
				linha = 2 if (linha == 3) else linha
				numCubos += 1
				largaBloco(move_garra, move_tank)
				if(atualiza):
					move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), 0.15)
			else:
				# Sem cubo, só virar pra continuar normal
				print("----------", linha)
				if(linha != 7):
					move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)
				elif(recupera != 0 and recupera != 2):
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
						flagDrift = 0
					atualiza = True # Mudou de lateral	



		if(atualiza):
			# Está em uma nova lateral, reconfigurar o movimento
			lateral = lateral - 1 if (lateral != 1) else 4 # Rotação anti-horária de laterais
			if(lateral == 4):
				vaiNaLoca = True
			linha = 2 # Sempre vai começar na linha 2
			print("AQUI 1")
			if flagDrift == 0:
				print("AQUI 2")
				move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90) # Vira pra arena
				move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 1.5) # Ré na parede 
				move_tank.on_for_rotations(SpeedPercent(VEL), SpeedPercent(VEL), 0.2) # Ajustar
			else:
				flagDrift = 0
			motorEsq.reset()
			motorDir.reset()
			sleep(0.3)
			comCubo = verificaLinha(move_tank, ultrassom, colorE, colorD, motorEsq, motorDir, linha) # Aproveita pra procurar um cubo na linha
			atualiza = False
		elif(comCubo):
			# Deixou um cubo, mas continua na mesma lateral
			distRodas = 0
			move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)
			move_tank.on_for_rotations(SpeedPercent(-VEL), SpeedPercent(-VEL), 1.2)
			move_tank.on_for_rotations(SpeedPercent(VELROT), SpeedPercent(-VELROT), ROT90)
			motorEsq.reset()
			motorDir.reset()
			move_tank.on(SpeedPercent(VEL), SpeedPercent(VEL))
			# Anda até a lateral que achou o cubo
			while((((linha-2)*N) - distRodas) > 10):
				# Como ao deixar o cubo ele se encontra na linha '2', precisa basear a distancia a ser andada nisso
				distRodas = int((motorEsq.position + motorDir.position)/2)
				if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and filterultrassom(ultrassom) > 310):
					# Alinha, enquanto longe da parede
					alinhaTempo(colorE, colorD, VEL, move_tank, False)
			if(linha == 7):
				move_tank.on_for_rotations(SpeedPercent(-VELROT), SpeedPercent(VELROT), ROT180)
				motorEsq.reset()
				motorDir.reset()
				sleep(0.3)
				comCubo = verificaLinha(move_tank, ultrassom, colorE, colorD, motorEsq, motorDir, linha) # Aproveita pra procurar um cubo na linha
			else:
				comCubo = False
	return

if __name__ == '__main__':
	motorEsq = LargeMotor(OUTPUT_C)
	motorDir = LargeMotor(OUTPUT_D)
	sound = Sound()
	lavanderias = lavanderias = [[1 for i in range(2)] for j in range(2)] # Todas as matrizes começam livres
	lateral = 0

	print("GO")

	sound.beep() #Beeep
	
	move_garra, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias, lateral, numCubos, move_steering = setRobot(lavanderias)
	controla(numCubos, lateral)

	motorDir.reset()
	motorEsq.reset()
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