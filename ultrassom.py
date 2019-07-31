from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from time import sleep

ultrassom = UltrasonicSensor(INPUT_1)
move_tank = MoveTank(OUTPUT_C, OUTPUT_D)

move_tank.on(SpeedRPM(40), SpeedRPM(40))

while True:

    distancia = 0
    distancia2 = 0
    contador = 0

    while(contador < 3):
        distancia += ultrassom.value()
        contador += 1
    distancia = int(distancia)

    print("--------------------------------------")
    print('ultrassom: ', (distancia))

    if distancia < 150:
        move_tank.on(SpeedRPM(0), SpeedRPM(0))
        break

    sleep(0.5)