from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from statistics import mode
import time

# Definindo o nome das cores da matriz de cores
Preto = 0
Branco = 1

# Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

# Disponibilidade
Livre = True
Ocupada = False

tempo_centro_quadrado = 1  # Esse é o tempo que ele precisa para chegar ao centro do quadrado
dist_max = 2100  # Essa é a distância do primeiro ao último quadrado da linha


def descerLateral():
    # Inicialização de motores
    move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
    colorF = ColorSensor(INPUT_2)
    colorE = ColorSensor(INPUT_3)
    colorD = ColorSensor(INPUT_4)
    colorE.mode = 'COL-COLOR'  # O sensor está vendo por cor (modo)
    colorD.mode = 'COL-COLOR'
    move_tank.on(SpeedRPM(20), SpeedRPM(20))

    while True:
        # Filtro para cor de leitura #
        colorListE = list()
        colorListD = list()
        contador = 0
        while (contador < 3):
            colorListE.append(colorE.value())
            colorListD.append(colorD.value())
            contador += 1
        print("moda esquerda: ", mode(colorListE))
        print("moda direita: ", mode(colorListD))

        if (mode(colorListE) == COLOR_BLACK and mode(
                colorListD) == COLOR_BLACK):  # Pensar em quando está em cima do bloco quadrado preto
            iniTime = time.clock()
            while ((time.clock() - iniTime) < tempo_centro_quadrado):
                print(time.clock() - iniTime)
                contador = 0
            move_tank.on(SpeedRPM(0), SpeedRPM(0))
            move_tank.on_for_rotations(SpeedRPM(30), SpeedRPM(-30), 1.05)
            break


def verificaLinha():
    move_tank = MoveTank(OUTPUT_C, OUTPUT_D)

    ultrassom = UltrasonicSensor(INPUT_1)
    contador = 0
    distancia = 0
    g = 0
    while (contador < 5):
        distancia += ultrassom.value()
        contador += 1
        g = ultrassom.value()
        print(g)
    distancia = int(distancia / 5)
    print("Distancia final: ", distancia)
    if (distancia < dist_max):  # Pode ser que o cubo esteja no último quadrado
        print(1)
        return True
    else:
        print(0)
        move_tank.on_for_rotations(SpeedRPM(-30), SpeedRPM(30), 1.05)
        return False

def irAoCubo():
    tank_drive = MoveTank(OUTPUT_C, OUTPUT_D)
    ultrassom = UltrasonicSensor(INPUT_1)  # Reinicializacao
    garra1 = Motor(OUTPUT_A)  # garraE
    garra2 = Motor(OUTPUT_B)  # garraD
    # Sem aplicar modo no leitor frontal
    sensorFrontal = ColorSensor(INPUT_2)  # colorF

    tank_drive.on(SpeedRPM(40), SpeedRPM(40))  # inicia movimento

    while (ultrassom.value() > 130):
        pass

    tank_drive.on(SpeedRPM(0), SpeedRPM(0))  # para movimento
    pegaBloco(garra1, garra2, tank_drive, 1, coresLavanderias, lavanderias,
              sensorFrontal)  # função de aproximar e pegar o bloco
    tank_drive.on_for_rotations(SpeedPercent(-50), SpeedPercent(-50), 2)  # 360 para teste
    largaBloco(garra1, garra2, tank_drive)  # função que afasta e larga o bloco

