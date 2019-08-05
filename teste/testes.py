from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time


tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)  
ultrassom = UltrasonicSensor(INPUT_1)
garra1 = Motor(OUTPUT_A)
garra2 = Motor(OUTPUT_C)
#garra = MoveTank(garra1, garra2)

#garra.on_for_rotations(SpeedPercent(-10), 0.5)

tank_drive.on(SpeedPercent(20),SpeedPercent(20))

while(ultrassom.value() > 50):
	g=1
tank_drive.on(SpeedPercent(0),SpeedPercent(0))
	#garra.on_for_rotations(SpeedPercent(-10),SpeedPercent(10), 0.5)
garra1.on_for_rotations(SpeedPercent(-10), 0.1)
garra2.on_for_rotations(SpeedPercent(10), 0.1)
tank_drive.on_for_rotations(SpeedPercent(100),SpeedPercent(0), 4)
tank_drive.on_for_rotations(SpeedPercent(50),SpeedPercent(50), 1)
garra1.on_for_rotations(SpeedPercent(10), 0.1)
garra2.on_for_rotations(SpeedPercent(-10), 0.1)
tank_drive.on_for_rotations(SpeedPercent(-50),SpeedPercent(-50), 2)