

import RPi.GPIO as GPIO

class Float_Switch:
    
    pin = None # BOARD
    name = None

    def __init__(self, name, pin): # using GPIO.BOARD
        self.pin = pin
        self.name = name

        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled low (off)
 
    