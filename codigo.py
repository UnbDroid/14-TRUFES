#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import time

def acharHome():
	"Acha o primeiro quadrado e define a posição atual"
	dist = ultraSense.value()
#	tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(40), 0.666)
	tank_drive.on(SpeedPercent(20),SpeedPercent(20))
	
	while dist > 190: #Aqui iria o sensor de distância
		dist = ultraSense.value()
		print("Procurando parede")
		print(dist)

	tank_drive.off()
	cor = colorbaixo.value() #Sensor pra ver a cor da lavanderia
	return cor

# def procuraCubo(arena_arg, posiat_arg, posian_arg):
# 	"Percorre o grid, marcando os espaços percorridos"
# 	achar = 0 #sensor de distância, verficar cubos
# 	while achar != 1:
# 		if posi_arg[1] == 7:
# 			#Avançar para a próxima linha
# 			tank_drive.on_for_rotations(SpeedPercent(-70),SpeedPercent(70), 0.666) #Vira pra esquerda
# 			tank_drive.on_for_rotations(SpeedPercent(70),SpeedPercent(70), 2.252)  #Avança
# 			tank_drive.on_for_rotations(SpeedPercent(-70),SpeedPercent(70), 0.666) #Vira pra esquerda
# 			tank_drive.on_for_rotations(SpeedPercent(-80),SpeedPercent(-80), 1.8)  #Ré, alinha com parede
# 			posiat_arg[0] += 1
# 			posian_arg[1] = (posiat_arg[1] < posian_arg[1]) ? posian_arg[1]+2
# 		tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 2.252)
# 		if posiat_arg[1] < posian_arg[1]:
# 			posian_arg[1] = posiat_arg[1]
# 			posiat_arg[1] -= 1
# 		else:
# 			posian_arg[1] = posiat_arg[1]
# 			posiat_arg[1] += 


ultraSense = UltrasonicSensor(INPUT_1)
#colorfrente = ColorSensor(INPUT_2)
coloresq = ColorSensor(INPUT_3)
colordir = ColorSensor(INPUT_4)
motoresq = LargeMotor(OUTPUT_B)
motordir = LargeMotor(OUTPUT_D)
tank_drive = MoveTank(OUTPUT_B, OUTPUT_D)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

arena = [[0] * 8 for i in range(8)]
posi_at = [6,1] #y,x
posi_an = [7,1]
u = 200
#motoresq.reset()
#motordir.reset()

#corInicial = acharHome()
# tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(-40), 0.666)
# tank_drive.on_for_rotations(SpeedPercent(60),SpeedPercent(60), 0.5)
# tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(-40), 0.666)

# while a < 1200:
# 	a = motor1.position
#  	b = motor2.position
#  	andado = (a+b)/2
#tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 2.252*8)
# while achar != 1:
# 		if posi_arg[1] == 7:
# 			tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(40), 0.666)
# 			tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 2.273)
# 			tank_drive.on_for_rotations(SpeedPercent(-40),SpeedPercent(40), 0.666)
# 			posi_arg[0] -= 1
# 		elif posi_arg[1] == 0:
#print(corInicial)
#tank_drive.on_for_rotations(SpeedPercent(90),SpeedPercent(90), 0.1)
#tank_drive.on(SpeedPercent(0),SpeedPercent(0))
#time.sleep(1)
#tank_drive.on_for_rotations(SpeedPercent(40),SpeedPercent(40), 0.2)
#tank_drive.on(SpeedPercent(25),SpeedPercent(0))
#time.sleep(1)
#tank_drive.on(SpeedPercent(0),SpeedPercent(0))
while(u > 60):
	e = coloresq.value()
	d = colordir.value()
	u = ultraSense.value()
	print(e, "Esquerda")
	print(d, "Direita")
	print(u, "Dist")
	tank_drive.on(SpeedPercent(5),SpeedPercent(5))
	time.sleep(0.4)

tank_drive.on(SpeedPercent(0),SpeedPercent(0))
	# delta = a - b  
	# potr -= delta*0.005+int_delta*0.0000034
	# potl += delta*0.005+int_delta*0.0000034

	# if potr > 50:
	# 	potr = 50
	# 	pass

	# if potl > 50:
	# 	potl = 50
	# 	pass

	# motor1.on(SpeedPercent(potr))
	# motor2.on(SpeedPercent(potl))

		
	# if a < (b + 18):
	# 	while a < (b + 18):
	# 		motor1.on(SpeedPercent(40))
	# 		motor2.on(SpeedPercent(37))
	# 		a = motor1.position
	# 		b = motor2.position
	# elif (b + 18) < a:
	# 	while (b + 18) < a:
	# 		motor1.on(SpeedPercent(37))
	# 		motor2.on(SpeedPercent(40))
	# 		a = motor1.position
	# 		b = motor2.position
	# else:
	# 	motor1.on(SpeedPercent(40))
	# 	motor2.on(SpeedPercent(40))
#print(s)
#tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50),0.1)
#tank_drive.on(SpeedPercent(0), SpeedPercent(0))
#tank_drive.on_for_rotations(SpeedPercent(40), SpeedPercent(40),1.67)
#tank_drive.on_for_rotations(SpeedPercent(-40), SpeedPercent(0),1.25)
#tank_drive.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 3.7)

