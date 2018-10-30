 
import RPi.GPIO as GPIO

import time

from push_button import Push_Button

button_list = {
    "LIFT" : 38,  #BCM
    "LOWER" : 36,
    "BYPASS" : 22,
    "STOP" : 32,
}

class Push_Buttons:

    list = {}

    def __init__(self,set_mode_callback): # using GPIO.BOARD
        for name,bcm in button_list.items():
            def callback(pin):
                print ("pushed " + name)
                set_mode_callback(name)
            self.list [name] = Push_Button (bcm, callback)
    

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    def callback (name):
        print (name)
    pbs = Push_Buttons (callback)
    while True:
        pass

