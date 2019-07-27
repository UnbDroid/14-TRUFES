'''MAPEAMENTO DA ARENA:'''

Col2 = 0
#Col2 é a variavel que mede se a colun possui mais de um cubo. se 0, nao. se 1, sim
if Col2 == 1:
    #ROBO SE DESLOCA PARA OUTRA COLUNA
else:
    #O ROBO SE APROXIMA, VE A COR DO BLOCO, O AGARRA E SEGUE RETO ATE UMA PAREDE
    #VIRA A DIREITA SE A LAVANDERIA DA RESPECTIVA COR ESTIVER A DIREITA E IDEM A ESQUERDA

'''ALINHAMENTO COM O BLOCO:'''

#D é uma variavel de distancia do robo.
D = 30
if D <= 30:
    #O ROBO ROTACIONA PARA OS DOIS LADOS, DIREITA E ESAUERDA, COMO SE BALANCASSE A CABECA
    #A PARTIR DISSO, O ROBO ANDA DESALINHADO COM O GRID ATÉ ACHAR O BLOCO E IDENTIFICAR A COR
    #ELE PEGA O BLOCO, REALINHA COM O GRID VOLTANDO A ANGULACAO INICIAL E SEGUE RETO ATE UMA PAREDE
    #VIRA A DIREITA SE A LAVANDERIA DA RESPECTIVA COR ESTIVER A DIREITA E IDEM A ESQUERDA


def organizaCubos(arena, ultra, sensorEsq, sensorDir, motorEsq, motorDir):
	"Recebe a Arena mapeada e busca os cubos"
	#Gravar a posicao inicial do robo baseado no '3' na arena (Usar dois 'for's pra iterar e descobrir?)
	#Iniciar um loop ate entregar todos os cubos
		#Existe cubo na minha linha/coluna (dependendo do deslocamento em X ou Y)?
		 	#Sim, existe mais de um?
		 		#Sim, passar pra próxima linha/coluna e não apagar o '2' (Opcao: apenas mudar o caminho pra desviar do segundo cubo?)
				#Não, virar pra esquerda, ir ate o cubo, *alinhar*, apagar o '2' e descobir a cor
					#Existe uma lavanderia disponível dessa cor, se eu for reto? (Ver se o robo partiu de uma coordenada 7 ou 0?)
						#Sim, continuar reto, virar pro lado correspondente e entregar
						#Nao, dar re, virar pro lado correspondente e entregar
			#Nao, passar direto pra proxima linha/coluna

	#Se chegou aqui, desafio completo

### Fazer redundância com o ultrassom de novo, pra não se perder?
### Manter a funcao de alinhamento rodando em todas as partes do processo (não usar movimento por segundos/rotações)