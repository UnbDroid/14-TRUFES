from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from inicializacao import iniciar

garraE, garraD, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias = iniciar()
disponibilidadeLavanderias = [[1 for i in range(2)] for j in range(2)] # Todas lavanderias iniciam disponíveis

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