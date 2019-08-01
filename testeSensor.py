from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

#garra1 = Motor(OUTPUT_A)
#garra2 = Motor(OUTPUT_B)
#garra1.on_for_rotations(SpeedPercent(-10), 0.2) #garra da esquerda abre
#garra2.on_for_rotations(SpeedPercent(10), 0.2) #garra da direita abre

colorsenseF = ColorSensor(INPUT_2)
#colorsenseF.MODE_RGB_RAW


while True:
    print("Front: ", colorsenseF.value())
    #print("Esquerda: ", colorsenseE.value())
    #print("Direita: ", colorsenseD.value())
    time.sleep(0.5)