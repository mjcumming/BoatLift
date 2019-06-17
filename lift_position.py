"""

determines position of the lift (height)

lift has 3 defined positions

LOWERED
LIFTED
LIFTEDMAX


float switch version

Pins 16,18,22

"""
import RPi.GPIO as GPIO

import time

from threading import Timer

from float_switch import Float_Switch

float_switch_list = {
    "BOTTOM" : 16,  #BOARD
    "MIDDLE" : 18,
    "TOP" : 22,
}

class Lift_Position:

    float_switches = {}
    callback = None
    timer = None

    def __init__(self,position_callback): # using GPIO.BOARD
        self.callback = position_callback

        def debounce(channel):
            print ('float switch callback',channel, GPIO.input(channel))
            if self.timer:
                self.timer.cancel()
            
            def callback():
                self.callback(self.get())

            self.timer = Timer(5,callback)
            self.timer.start()

        for name,pin in float_switch_list.items():
            self.float_switches [name] = Float_Switch(name,pin)
            GPIO.add_event_detect(pin,GPIO.BOTH,callback=debounce, bouncetime=1) # Setup event on pin rising edge

    def read_float_switches(self):
        switches = {}
        for name,float_switch in self.float_switches.items():
            switches [name] = float_switch.read()

        return switches

    def get(self): #returns the position of the lift
        switches = self.read_float_switches()

        print('Float switches: {}'.format(switches))

        if switches ["BOTTOM"] == "OutOfWater" and switches ["MIDDLE"] == "OutOfWater" and switches ["TOP"] == "OutOfWater":
            return "LIFTEDMAX"
        elif switches ["BOTTOM"] == "InWater" and switches ["MIDDLE"] == "OutOfWater" and switches ["TOP"] == "OutOfWater":
            return "LIFTED"
        elif switches ["BOTTOM"] == "InWater" and switches ["MIDDLE"] == "InWater" and switches ["TOP"] == "OutOfWater":
            return "BETWEENLOWEREDLIFTED"
        elif switches ["BOTTOM"] == "InWater" and switches ["MIDDLE"] == "InWater" and switches ["TOP"] == "InWater":
            return "LOWERED"
        else:
            return "ERROR UNKNOWN"

    def is_lifted(self):
        return self.get()=='LIFTED'

    def is_lifted_max(self):
        return self.get()=='LIFTEDMAX'

    def is_lowered(self):
        return self.get()=='LOWERED'

   

if __name__ == "__main__":
    
    GPIO.setmode(GPIO.BOARD)
    def callback (name):
        print ("Lift Position: "+name)

    pbs = Lift_Position(callback)

    print (pbs.get())
 

    while True:
        pass

