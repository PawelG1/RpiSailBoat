from math import degrees
import pigpio
import time

pi = pigpio.pi()


class sailWinch():

    

    def __init__(self):
        self.rots = 1
        self.rev = 1320*(2.1) #1320 -> 2640
        self.maxSteps = 10
        self.timeDelay = 0.00100 #max delay 0.00010        
        self.prev_val = 0
        self.actSteps = 0


    def rotation(self, in_val):
    
        deg = ((in_val - 0) * (self.rev - 0) / (180 - 0) + 0)
        deg = deg - self.prev_val
        self.actSteps = 0
        self.prev_val = deg
        
        if(deg > 0):

            pi.write(13, pigpio.HIGH)

            while(1==1):

                print("wybieranie")

                if(self.actSteps <= deg):
                    pi.write(19, 1)
                    self.actSteps +=  1
                    time.sleep(self.timeDelay)

                if(self.actSteps <= deg):
                    pi.write(19, 0)
                    self.actSteps += 1
                    time.sleep(self.timeDelay)

                if(self.actSteps > deg):
                    self.actSteps = 0
                    break

                f = open(r"/home/pi/SailboatSoft/OLD/variable.txt", 'w')
                f.write(str(self.actSteps))
                f.close()

                print(self.actSteps)

        elif(deg < 0):
            deg = -deg
            pi.write(13, pigpio.LOW)
        
            while(1==1):
                print("luzowanie")
            
                if(self.actSteps <= deg):
                    pi.write(19, 0)
                    self.actSteps += 1
                    time.sleep(self.timeDelay)

                if(self.actSteps <= deg):
                    pi.write(19, 1)
            
                    self.actSteps +=  1
                    time.sleep(self.timeDelay)    
                
                if(self.actSteps > deg):
                    self.actSteps = 0
                    break

                f = open(r"/home/pi/SailboatSoft/OLD/variable.txt", 'w')
                f.write(str(self.actSteps))
                f.close()

                print(self.actSteps)
                

    def winch_rs(self):
        f = open(r"/home/pi/SailboatSoft/OLD/variable.txt", 'r')
        last_pos = int(f.read())

        print("ile cofnac")
        go_back = (self.rev - last_pos)
        print(go_back)
        
        deg = go_back
        pi.write(13, pigpio.LOW)
        
        while(1==1):
            print("luzowanie")
            
            if(self.actSteps <= deg):
                pi.write(19, 0)
                self.actSteps += 1
                time.sleep(self.timeDelay)
            if(self.actSteps <= deg):
                pi.write(19, 1)
            
                self.actSteps +=  1
                time.sleep(self.timeDelay)
            if(self.actSteps > deg):
                self.actSteps = 0
                break

            


        time.sleep(3)

if __name__ == '__main__':

    tak = sailWinch()
    tak.winch_rs()

    tak.rotation(180)
    time.sleep(5)
    tak.rotation(0)


