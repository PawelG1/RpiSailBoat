from math import degrees
import pigpio
import time
import json
pi = pigpio.pi()

class stepper():
	def __init__(self) -> None:
		self.STEP_PIN = 19
		self.DIR_PIN = 13
		self.stepPTurn = 1324 #steps per 1 turn
		#stepper motor steps per rotation =200 , gearbox ratio 324/49
		self.delay = 0.0025

	def savepos(self, pos):
		f = open("/home/pi/SailboatSoft/SailSoft/stepper_pos.json")
		last_pos = json.load(f)
		f.close
		last_pos = int(last_pos['pos'])
		print(last_pos)
		pos = pos + last_pos
		print(pos)
		data = {
			"pos": pos
		}
		with open("/home/pi/SailboatSoft/SailSoft/stepper_pos.json", "w") as outfile:
			json.dump(data, outfile)


	def pull(self, degrees): # input have to be in degrees
		steps = int((degrees / 360) * self.stepPTurn)
		
		pi.write(self.DIR_PIN, pigpio.HIGH)

		for i in range(steps):
			time.sleep(self.delay)
			pi.write(self.STEP_PIN, 1)
			time.sleep(0.00001)
			pi.write(self.STEP_PIN, 0)

		time.sleep(0.00001)

		self.savepos(degrees)

		pi.write(self.DIR_PIN, pigpio.LOW)
	

			
	def loosen(self, degrees):
		steps = int((degrees / 360) * self.stepPTurn)

		pi.write(self.DIR_PIN, pigpio.LOW)

		for i in range(steps):
			time.sleep(self.delay)
			pi.write(self.STEP_PIN, 1)
			time.sleep(0.00001)
			pi.write(self.STEP_PIN, 0)

		time.sleep(0.00001)

		self.savepos(-degrees)


if __name__ == '__main__':

	winch = stepper()
	delay = 0.01
	STEP_PIN = 19 
	pi.write(13, pigpio.HIGH)


	#winch.pull(360)
	time.sleep(2)
	winch.loosen(360)

	

	"""for i in range(1000):
		time.sleep(delay)
		pi.write(19, 1)
		print("1")
		time.sleep(0.001)
		pi.write(19, 0)
		print("0")
	"""

	  
	