 
import RPi.GPIO as GPIO

import time

from push_button import Push_Button

button_list = {
    "LIFT" : 38,  #BOARD
    "LOWER" : 36,
    "BYPASS" : 22,
    "STOP" : 32,
}

class Push_Buttons:

    buttons = {}
    pin_to_mode = {}

    def __init__(self,set_mode_callback): # using GPIO.BOARD
        def callback(pin):
            set_mode_callback(self.pin_to_mode [pin])

        for mode,pin in button_list.items():
            self.buttons [mode] = Push_Button(mode,pin)
            self.pin_to_mode [pin] = mode
            GPIO.add_event_detect(pin,GPIO.RISING,callback=callback, bouncetime=500) # Setup event on pin rising edge

   

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    def callback (name):
        print ("Button Pushed: "+name)

    pbs = Push_Buttons(callback)
    while True:
        pass

