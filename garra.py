from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

def pegaBloco(garra1, garra2, tank_drive):
	garra1.on_for_rotations(SpeedPercent(10), 0.2) #garra da esquerda abre
	garra2.on_for_rotations(SpeedPercent(-10), 0.2) #garra da direita abre
	tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(20), 0.5) #movimenta com base em 125mm de distância do cubo
	garra1.on_for_rotations(SpeedPercent(-10), 0.2) #garra da esquerda fecha
	garra2.on_for_rotations(SpeedPercent(10), 0.2) #garra da direita fecha

def largaBloco(garra1, garra2, tank_drive):
	garra1.on_for_rotations(SpeedPercent(10), 0.2) #garra da esquerda abre
	garra2.on_for_rotations(SpeedPercent(-10), 0.2) #garra da direita abre
	tank_drive.on_for_rotations(SpeedPercent(-20),SpeedPercent(-20), 0.5) #ré com base em 125mm de distância do cubo
	garra1.on_for_rotations(SpeedPercent(-10), 0.2) #garra da esquerda fecha
	garra2.on_for_rotations(SpeedPercent(10), 0.2) #garra da direita fecha

if __name__ == '__main__':
	tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)  
	ultrassom = UltrasonicSensor(INPUT_1)
	garra1 = Motor(OUTPUT_A)
	garra2 = Motor(OUTPUT_C)
	
	tank_drive.on(SpeedRPM(20), SpeedRPM(20)) #inicia movimento
	while(ultrassom.value() > 125):
		g=1
	tank_drive.on(SpeedRPM(0), SpeedRPM(0)) #para movimento
	pegaBloco(garra1, garra2, tank_drive) #função de aproximar e pegar o bloco
	tank_drive.on_for_rotations(SpeedPercent(-100),SpeedPercent(0), 4) # 360 para teste
	largaBloco(garra1, garra2, tank_drive) #função que afasta e larga o bloco

