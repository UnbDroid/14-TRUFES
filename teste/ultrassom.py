from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from time import sleep

ultrassom = UltrasonicSensor(INPUT_1)

while True:

	distancia = 0
	contador = 0

	timeini = time.clock()
	while(contador < 10):
		distancia += ultrassom.value()
		contador += 1
	distancia = int(distancia/10)
	timend = time.clock()
	print("--------------------------------------")
	print('ultrassom: ', (distancia))
	print('Tempo:', timend - timeini)
	if ((time.clock() - timeini) > 10):
		break
	sleep(1)