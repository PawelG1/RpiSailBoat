#!/usr/bin/env python3
import mechanics
from threading import Thread
import winch_mod as winch
import time
import db_connection
import nanoconn as nc
import math
import json
import requests


db_connection.connect_to_db()



# tak = winch.sailWinch() will be added in future
# tak.winch_rs()
time.sleep(2)


class autonomous:
	def __init__(self) -> None:
		self.sData = nc.dataFAtmega()
		self.sData.get_data()
		self.rud_error = 0
		self.rud_prev_error = 0
		self.sum_errors = 0
		self.declination = 0

		self.rudder_val = 0  # rudder_val can be in range(-90, 90)

		self.t1 = Thread(target=mechanics.rudder_servo, args=(0,))
		self.t1.start()
		self.t2 = Thread(target=mechanics.boom_servo, args=(0,))
		self.t2.start()

		self.timeFromLastReq = time.time()
		self.pidTime = time.time()

		f = open("private.json")
		self.KEYS = json.load(f)
		f.close

		f = open("/home/pi/SailboatSoft/SailSoft/pidParams.json")
		self.PID = json.load(f)
		f.close
		self.dTime = self.PID["dt"]

	def getDeclination(self):
		lat1 = "lat1=" + str(self.sData.lat)
		lon1 = "lon1=" + str(self.sData.lon)
		KEY = "key=" + self.KEYS["key"]
		RESULT_FORMAT = "resultFormat=" + "json"
		BASE_ADDRESS = (
			"https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination?"
		)

		params = [BASE_ADDRESS, lat1, lon1, KEY, RESULT_FORMAT]
		address = "&".join(params)
		response = requests.get(address)
		if response.status_code != requests.codes.ok:
			print("something went wrong")
			print(address)
		else:
			magData = response.json()
			self.declination = magData["result"][0]["declination"]
			self.timeFromLastReq = time.time()
		return self.declination

	def setCourse(self):
		KP = self.PID["KP"]
		KI = self.PID["KI"]
		KD = self.PID["KD"]
		maxRudderVal = (180 * KP) + (179 * KD) + (180 + 179) * KI

		dest = db_connection.get_dest()

		lat = dest["lat"]
		lon = dest["lon"]
		deltaLat = self.sData.lat - lat
		deltaLon = self.sData.lon - lon
		kurs = math.atan2(deltaLat, deltaLon) * (180 / math.pi)

		if kurs < 0:  # transform course from range(-180,180) to range(0,360)
			kurs = (180 + kurs) + 180

		if (
			self.sData.heading <= 360
		):  # if heading data received from serial is correct then use regulator

			azimuth = self.sData.heading
			self.rudder_val = (
				0
				+ (self.rud_error * KP)
				+ (self.rud_prev_error * KD)
				+ ((self.sum_errors) * KI)
			)
			self.rud_prev_error = self.rud_error
			self.rud_error = kurs - azimuth

			if self.rud_error > 180:
				self.rud_error = self.rud_error - 360

			self.sum_errors += self.rud_error

			print("rudder error :", self.rud_error)
			
			self.rudder_val = int((self.rudder_val / maxRudderVal) * 90)

		return self.rudder_val

	def refresh(self):
		self.data = db_connection.get_data()
		self.sData.get_data()  # gets package of data from sensors

		if (
			(time.time() - self.timeFromLastReq) > 5
			and self.sData.lat != 0
			and self.sData.lon != 0
		):
			self.getDeclination()  # gets declination data for actual position
			print(self.sData.lat)


		self.sData.heading = (
			self.sData.heading + self.declination
		)  # corrects heading with declination data

		print("Heading = ", self.sData.heading)
		print("wind direction = ", self.sData.windir)

		if (time.time() - self.pidTime) > self.dTime:
			print("rudderVal = ", self.setCourse())
			self.pidTime = time.time()

		if not self.t1.is_alive():
			self.t1 = Thread(target=mechanics.rudder_servo, args=(self.rudder_val,))
			self.t1.start()


class remoteSteer:
	def __init__(self) -> None:
		self.t1 = Thread(target=mechanics.rudder_servo, args=(0,))
		self.t1.start()
		self.t2 = Thread(target=mechanics.boom_servo, args=(0,))
		self.t2.start()

	def refresh(self):
		self.data = db_connection.get_data()
		print("rudder value is %s" % (self.data["rudder"]))
		print("navi_lights value is %s" % (self.data["navi_lights"]))
		print("boom_angle value is %s" % (self.data["boom_angle"]))
		print("motor value is %s" % (self.data["motor"]))
		print("anchor value is %s" % (self.data["anchor"]))

		if not self.t1.is_alive():
			self.t1 = Thread(target=mechanics.rudder_servo, args=(self.data["rudder"],))
			self.t1.start()

	def isCaptainAlive(self):
		try:
			x = self.data["anchor"]
			return x
		except:
			print("call refresh method first")


if __name__ == "__main__":
	data = db_connection.get_data()

	if data["anchor"] == 1:
		captain = autonomous()
		while True:
			captain.refresh()
	else:
		captain = remoteSteer()
		while True:
			captain.refresh()
			if captain.isCaptainAlive() == 1:
				break
