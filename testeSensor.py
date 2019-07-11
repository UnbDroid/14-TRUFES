from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

colorsenseE = ColorSensor(INPUT_3)
colorsenseD = ColorSensor(INPUT_4)

while True:
    print("Esquerda: ", colorsenseE.value())
    print("Direita: ", colorsenseD.value())
    time.sleep(0.5)