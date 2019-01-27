"""


InWater = 0
OutOfWater = 1


"""

import RPi.GPIO as GPIO
import time


class Float_Switch:
    
    pin = None # BOARD
    name = None

    def __init__(self, name, pin): # using GPIO.BOARD
        self.pin = pin
        self.name = name

        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled low (off)
 

    def read(self):
        #print ('float read',self.name,GPIO.input(self.pin))
        return (GPIO.input(self.pin) == 1) and "OutOfWater" or "InWater"
    


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    float = Float_Switch ("Test", 40)
 
    while True:
        print("Float {}, position {}".format(float.name,float.read()))        
        time.sleep (.5)
