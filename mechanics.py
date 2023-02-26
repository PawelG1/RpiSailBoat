from logging import raiseExceptions
import pigpio
import time
import winch_mod as winch


pi = pigpio.pi()
rudder = pigpio.pi()
prev_val = 0
pi.set_PWM_frequency(12, 330)

rudder.set_mode(12, pigpio.ALT5) 
boom = pigpio.pi()

tak = winch.sailWinch()
tak.winch_rs()
time.sleep(4)

def rudder_servo(in_val):
	in_val = in_val - 5
	if(in_val >= 36):
		in_val = 35
	if(in_val <= -56):
		in_val = -55
	in_val = in_val+90
	val = ((in_val - 0) * (2500 - 500) / (180 - 0) + 500)
	rudder.set_servo_pulsewidth(12, val)
	time.sleep(0.9)


def boom_servo(in_val):
	tak.rotation(in_val)
	time.sleep(2.9)

def motor_on():
	pi.write(24, 1) #24[purple](2nd), 
	pi.write(25, 0) #25[blue](1st from lest on the board),  
	pi.write(23, 1) #23[green](3) on/off/pwm
 
def motor_off():
	pi.write(24, 0)
	pi.write(25, 0)
	pi.write(23, 0)#23[green](3)

def lights_on():
	pi.write(26, 1) #13 -> 26 2 pin on 
def lights_off():
	pi.write(26, 0)



if __name__ == "__main__":
	while True:
		try:
			lights_on()
			motor_on()
			time.sleep(5);motor_off()
			time.sleep(1)
			#boom_servo(90)
			time.sleep(3)
			lights_off()
			#boom_servo(180)
			time.sleep(3)
			rudder_servo(90)
			time.sleep(2)
			rudder_servo(0)
		except KeyboardInterrupt:

			print("test ended")
	
	pi.cleanup()