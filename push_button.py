

import RPi.GPIO as GPIO

class Push_Button:
    
    pin = None # BOARD

    def __init__(self, pin, button_callback): # using GPIO.BOARD
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled low (off)
        
        GPIO.add_event_detect(self.pin,GPIO.RISING,callback=button_callback, bouncetime=500) # Setup event on pin rising edge


    