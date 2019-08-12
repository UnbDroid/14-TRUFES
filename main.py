from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from inicializacao import iniciar
from achaCubo import *
from garra import *

garraE, garraD, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias = iniciar()
lavanderias = [[1 for i in range(2)] for j in range(2)] # Todas lavanderias iniciam disponíveis
comCubo = False
while(comCubo == False):
    descerLateral()
    comCubo = verificaLinha()

tank_drive = MoveTank(OUTPUT_C, OUTPUT_D)
ultrassom = UltrasonicSensor(INPUT_1) # Reinicializacao
garra1 = Motor(OUTPUT_A) # garraE
garra2 = Motor(OUTPUT_B) # garraD
# Sem aplicar modo no leitor frontal
sensorFrontal = ColorSensor(INPUT_2) # colorF

tank_drive.on(SpeedRPM(40), SpeedRPM(40))  # inicia movimento

while (ultrassom.value() > 130):
    pass

tank_drive.on(SpeedRPM(0), SpeedRPM(0))  # para movimento
pegaBloco(garra1, garra2, tank_drive, 1, coresLavanderias, lavanderias,
          sensorFrontal)  # função de aproximar e pegar o bloco
tank_drive.on_for_rotations(SpeedPercent(-50), SpeedPercent(-50), 2)  # 360 para teste
largaBloco(garra1, garra2, tank_drive)  # função que afasta e larga o bloco

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