 
import RPi.GPIO as GPIO

import time

from LED import LED 

LED_list = {
    "lift" : 7,  #BOARD
    "lower" : 11,
    "bypass" : 13,
    "stop" : 15,
}

class LEDs:

    list = {}

    def __init__(self): # using GPIO.BOARD
        for name,bcm in LED_list.items():
            self.list [name] = LED (bcm)
    
    def all_on (self):
        for name,LED in self.list.items():
            LED.on()

    def all_off (self):
        for name,LED in self.list.items():
            LED.off()

    def all_flash (self):
        for name,LED in self.list.items():
            LED.flash()

    def set_lift(self):
        self.list ["lift"].flash()
        self.list ["lower"].off()
        self.list ["bypass"].off()
        self.list ["stop"].on()

    def set_lower(self):
        self.list ["lift"].off()
        self.list ["lower"].flash()
        self.list ["bypass"].off()
        self.list ["stop"].on()

    def set_bypass(self):
        self.list ["lift"].off()
        self.list ["lower"].off()
        self.list ["bypass"].flash()
        self.list ["stop"].on()

    def set_lifted(self):
        self.list ["lift"].off()
        self.list ["lower"].on()
        self.list ["bypass"].on()
        self.list ["stop"].off()

    def set_lifted_max(self):
        self.list ["lift"].off()
        self.list ["lower"].on()
        self.list ["bypass"].on()
        self.list ["stop"].off()

    def set_lowered(self):
        self.list ["lift"].on()
        self.list ["lower"].off()
        self.list ["bypass"].on()
        self.list ["stop"].off()

    def set_unknown(self):
        self.list ["lift"].on()
        self.list ["lower"].on()
        self.list ["bypass"].on()
        self.list ["stop"].off()




if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    leds = LEDs ()
 
    while True:
        leds.all_on()
        #time.sleep (1)

        #leds.all_off()
        #time.sleep (1)

        #leds.all_flash()
        #time.sleep (10)        

        #leds.set_lift()
        time.sleep (10)        


