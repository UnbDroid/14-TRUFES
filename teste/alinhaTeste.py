from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from alinhamentoTempo import alinhaTempo

#Cores do sensor
COLOR_BLACK = 1
COLOR_WHITE = 6

ultrassom = UltrasonicSensor(INPUT_1)
move_garra = MoveTank(OUTPUT_A, OUTPUT_B, motor_class=MediumMotor)
move_tank = MoveTank(OUTPUT_C, OUTPUT_D)
colorE = ColorSensor(INPUT_3)
colorD = ColorSensor(INPUT_4)

move_tank.on(SpeedPercent(-40), SpeedPercent(-40))
print("passou")
print(ultrassom.value())
while (ultrassom.value() > 150):
	if(colorE.value() == COLOR_BLACK or colorD.value() == COLOR_BLACK):
		# Alinhamento
		alinhaTempo(colorE, colorD, 40, move_tank, True)
		print("Linha")
move_tank.on(SpeedPercent(0), SpeedPercent(0))