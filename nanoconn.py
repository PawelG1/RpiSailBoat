#!/usr/bin/env python3
from tkinter.messagebox import NO
import serial
import time
import queue


try:
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1) #top right port
    ser.reset_input_buffer()
except:

    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1) 
        ser.reset_input_buffer()
    except:
        ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=1) 
        ser.reset_input_buffer()
    
class dataFAtmega():


    def __init__(self) -> None:
        self.windir = 999
        self.heading = 999
        self.lat = 0
        self.lon = 0   
        self.time = time.time()     


    def get_data(self):
        line = None
        for i in range(1): # this loop tries for 10 times to get data from atmega
            
            if(line == None):
                
                if ser.in_waiting > 0:

                    line = None
                    line2 = ser.readline().decode('utf-8').rstrip()
                    line = line2.split(',')
                    self.windir = float(line[0])
                    self.heading = float(line[1])
                    self.lat = float(line[2])
                    self.lon = float(line[3])
                    self.time = time.time()
                    return 0
                
           
        #if method hasn't got any data from atmega and it was 5s since last data then set defaults
        if line == None and (time.time() - self.time )> 10:
            self.windir = 999
            self.heading = 999
            self.lat = 0
            self.lon = 0
                
                
             

if __name__ == "__main__":
    print("started")

    data = dataFAtmega()

    while True:
        
        data.get_data()
        print("-----------------------------------------")
        print("wind direction: ", data.windir)    
        print("Heading: ", data.heading)    
        print("latitude: ", data.lat)    
        print("longitude: ", data.lon)       

   

