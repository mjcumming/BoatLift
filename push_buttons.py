 
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

    def __init__(self,set_mode_callback): # using GPIO.BOARD

        for mode,pin in button_list.items():
            self.buttons [mode] = Push_Button(mode,pin,set_mode_callback)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    def callback (name,state):
        print ("Button Pushed: ",name,state)

    pbs = Push_Buttons(callback)
    while True:
        pass

