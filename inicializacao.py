from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from statistics import mode

#Definindo o nome das cores da matriz de cores
Preto = 0
Branco = 1

#Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

#Disponibilidade
Livre = True
Ocupada = False

def alinhaTempo(sensorE, sensorD, velocidade, tank_drive):
    print('alinhando')

    # Inicializando as variaveis de tempo
    leftTime = 0
    rightTime = 0

    #Inicializando as variaveis dos sensores de cor
    leftColor = sensorE.value()
    rightColor = sensorD.value()

    iniTime = time.clock()

    while((time.clock() - iniTime) < 0.7):
        leftColor = sensorE.value()
        rightColor = sensorD.value()
        if(leftColor == COLOR_BLACK):
            leftTime = time.clock()
            #print(leftTime, "LEFT")
        if(rightColor == COLOR_BLACK):
            rightTime = time.clock()
            #print(rightTime, "RIGHT")

    if(leftTime > rightTime):
        # Menor time = sair primeiro
        print(leftTime-rightTime)
        fixedTime = 2*(leftTime-rightTime+0.02)
        tank_drive.on_for_seconds(SpeedPercent(velocidade), SpeedPercent(velocidade/2),fixedTime) 
        tank_drive.on(SpeedPercent(velocidade), SpeedPercent(velocidade))
    if(leftTime < rightTime):
        # Menor time = sair primeiro
        fixedTime = 2*(rightTime-leftTime+0.02)
        print(rightTime-leftTime)
        tank_drive.on_for_seconds(SpeedPercent(velocidade/2), SpeedPercent(velocidade), fixedTime)        
        tank_drive.on(SpeedPercent(velocidade), SpeedPercent(velocidade))

def iniciar():
    # Inicialização de motores
    garraE = Motor(OUTPUT_A)
    garraD = Motor(OUTPUT_B)
    move_tank = MoveTank(OUTPUT_C, OUTPUT_D)

    # Inicialização de sensores
    ultrassom = UltrasonicSensor(INPUT_1)
    colorF = ColorSensor(INPUT_2)
    colorE = ColorSensor(INPUT_3)
    colorD = ColorSensor(INPUT_4)
    colorE.mode = 'COL-COLOR'
    colorD.mode = 'COL-COLOR'

    coresLavanderias = [[Preto for i in range(2)] for j in range(2)] # Todas lavanderias iniciam pretas

    move_tank.on(SpeedRPM(20), SpeedRPM(20))
    
    while True:
        
        # Filtrando o valor do ultrassom
        distancia = 0
        contador = 0

        while(contador < 5):
            distancia += ultrassom.value()
            contador += 1
        distancia = int(distancia/5)

        print("ultrassom: ", distancia)

        # Direcionando-se à primeira lavanderia

        if(distancia <= 145):
            move_tank.on_for_rotations(SpeedRPM(30), SpeedRPM(-30), 1.05)

            # Filtro para cor de leitura #
            colorListE = list()
            colorListD = list()
            contador = 0
            while(contador < 3):
                colorListE.append(colorE.value())
                colorListD.append(colorD.value())
                contador += 1
            print("moda esquerda: ", mode(colorListE))
            print("moda direita: ", mode(colorListD))

            if mode(colorListE) == COLOR_WHITE:
                corEsq = COLOR_WHITE
            else:
                corEsq = COLOR_BLACK
            if mode(colorListD) == COLOR_WHITE:
                corDir = COLOR_WHITE
            else:
                corDir = COLOR_BLACK
            ############################ Finalizando filtro ############################

            # Definindo a matriz de cores tendo em vista que ela foi iniciada totalmente preta
            print("dir: ", colorD.value())
            print("esq: ", colorE.value())
            print("ultrassom: ", ultrassom.value())

            # Preto
            if(corEsq == corDir and corEsq != COLOR_WHITE):
                print('op1')
                coresLavanderias[0][1] = Branco
                coresLavanderias[1][0] = Branco
                break
            # Branco
            elif(corEsq == corDir and corEsq != COLOR_BLACK):
                print('op2')
                coresLavanderias[0][0] = Branco
                coresLavanderias[1][1] = Branco
                break

        if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
            alinhaTempo(colorE,colorD,20,move_tank)

    print("Preto = 0 | Branco = 1")
    print('Superior esquerdo: ', coresLavanderias[0][0])
    print('Superior direito: ', coresLavanderias[0][1])
    print('inferior esquerdo: ', coresLavanderias[1][0])
    print('inferior direito: ', coresLavanderias[1][1])

    return garraE, garraD, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias


if __name__ == '__main__':

    garraE, garraD, move_tank, ultrassom, colorF, colorE, colorD, coresLavanderias = iniciar()