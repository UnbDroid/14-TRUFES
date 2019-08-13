from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from alinhamentoTempo import alinhaTempo
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
	motorEsq = LargeMotor(OUTPUT_C)
	motorDir = LargeMotor(OUTPUT_D)
	colorF = ColorSensor(INPUT_2)
	colorE = ColorSensor(INPUT_3)
	colorD = ColorSensor(INPUT_4)
	colorE.mode = 'COL-COLOR'  # O sensor está vendo por cor (modo)
	colorD.mode = 'COL-COLOR'

	motorEsq.reset()
	motorDir.reset()
	distMotores = 0

	move_tank.on(SpeedRPM(40), SpeedRPM(40))
	while(N - distMotores > 0):
		distMotores = int((motorEsq.position + motorDir.position)/2)
		if((colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK) and distancia > 310):
			alinhaTempo(colorE, colorD, 40, move_tank, False)


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
