import mysql.connector
import mechanics
from threading import Thread
import winch_mod as winch
import time
import db_connection
from simple_pid import PID
import nanoconn as nc
import math

db_connection.connect_to_db()


pid = PID(1, 0.1, 0.05, setpoint=1)

#tak = winch.sailWinch()
#tak.winch_rs()
time.sleep(2)

class autonomous():
	def __init__(self) -> None:
		self.sData = nc.dataFAtmega()
		self.t1 = Thread(target=mechanics.rudder_servo, args=(0,))
		self.t1.start()
		self.t2 = Thread(target=mechanics.boom_servo, args=(0,))
		self.t2.start()
		self.sData.get_data()
		self.rud_error = 0
		self.rud_prev_error = 0
		self.declination = 0
		
		
	def getDeclination(self):
		lat1 = 'lat1=' + str(self.sData.lat)
		lon1 = 'lon1=' + str(self.sData.lon)
		KEY = 'key=' +'zNEw7' 
		RESULT_FORMAT = 'resultFormat=' + 'json'
		
		params = [BASE_ADDRESS, lat1, lon1, KEY, RESULT_FORMAT]
		address = '&'.join(params)
		
		response = requests.get(address)
		if (response.status_code != requests.codes.ok):
    			print("something went wrong")
		else:
    			magData = response.json()
			self.declination = magData['result'][0]['declination']
		return self.declination
		
		

	def setCourse(self):
		KP = 2
		KI = 0.005
		KD = 0.01

		dest = db_connection.get_dest()

		lat = dest['lat']
		lon = dest['lon']
		deltaLat = self.sData.lat - lat
		deltaLon = self.sData.lon - lon
		kurs = math.atan2(deltaLat, deltaLon) * (180 / math.pi)


		if self.sData.heading <=360: 
			azimuth = self.sData.heading
	   
			self.rudder_val = 0 + (self.rud_error * KP) + (self.rud_prev_error * KD) + ( (self.rud_error + self.rud_prev_error) * KI ) 
			self.rud_prev_error = self.rud_error
			self.rud_error = (kurs - azimuth) 
	   
			self.rudder_val = (self.rudder_val) * (-1) 
			self.rudder_val = int(self.rudder_val)
		return self.rudder_val


	def refresh(self):	
		self.data = db_connection.get_data()
		self.sData.get_data()
		print("sailin")
		x = 10
		print(self.sData.heading)
		print("rudderVal = ", self.setCourse())

		if not self.t1.is_alive() :
			self.t1 = Thread(target=mechanics.rudder_servo, args=(x,))
			self.t1.start()


	
	

class remoteSteer():
	def __init__(self) -> None:
		self.t1 = Thread(target=mechanics.rudder_servo, args=(0,))
		self.t1.start()
		self.t2 = Thread(target=mechanics.boom_servo, args=(0,))
		self.t2.start()

	def refresh(self):	
		self.data = db_connection.get_data()
		print("rudder value is %s"% (self.data['rudder']))
		print("navi_lights value is %s"% (self.data['navi_lights']))
		print("boom_angle value is %s"% (self.data['boom_angle']))
		print("motor value is %s"% (self.data['motor']))
		print("anchor value is %s"% (self.data['anchor']))

		if not self.t1.is_alive() :
			self.t1 = Thread(target=mechanics.rudder_servo, args=(self.data['rudder'],))
			self.t1.start()


	def isCaptainAlive(self):
		try:
			x = self.data['anchor']
			return x
		except:
			print('call refresh method first')
		

if __name__=='__main__':
	data = db_connection.get_data()	

	if data['anchor'] == 1:
		captain = autonomous()
		while(True):
			captain.refresh()
	else:
		captain = remoteSteer()
		while(True):
			captain.refresh()
			if captain.isCaptainAlive() == 1:
				break
	



	


