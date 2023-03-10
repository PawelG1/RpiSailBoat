from logging import raiseExceptions
import pigpio
import time
from stepper import stepper
import json

pi = pigpio.pi()
rudder = pigpio.pi()
prev_val = 0
pi.set_PWM_frequency(12, 330)

rudder.set_mode(12, pigpio.ALT5) 


winch = stepper()
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


def boom_reset(in_val):
	f = open("/home/pi/SailboatSoft/SailSoft/stepper_pos.json")
	last_pos = json.load(f)
	f.close
	last_pos = int(last_pos['pos'])

	if(last_pos > 0):
		winch.loosen(last_pos)
		
	if(last_pos < 0):
		winch.pull(last_pos)

def boom_servo(in_val):
	val = ((in_val - 0) * (720 - 0) / (180 - 0) + 0)

	f = open("/home/pi/SailboatSoft/SailSoft/stepper_pos.json")
	last_pos = json.load(f)
	f.close
	last_pos = int(last_pos['pos'])

	if val > last_pos:
		winch.pull(val - last_pos)
	if val < last_pos:
		winch.loosen(last_pos - val)
	

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
			#lights_on()
			motor_on()
			time.sleep(3)
			motor_off()
			time.sleep(1)
			#boom_servo(0)
			#time.sleep(3)
			#lights_off()
			#boom_servo(180)
			#time.sleep(3)
			#rudder_servo(90)
			#time.sleep(2)
			#rudder_servo(0)
		except KeyboardInterrupt:

			print("test ended")
	
	pi.cleanup()