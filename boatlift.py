"""


Boat lift


"""


import RPi.GPIO as GPIO
import time

from roll_pitch import Roll_Pitch
from valves import Valves
from LEDs import LEDs
from push_buttons import Push_Buttons
from blower_motor import Blower_Motor

GPIO.setmode(GPIO.BOARD)

#request modes
LIFT = 1
LOWER = 2
BYPASS = 3
STOP = 4

# operating modes of lift
IDLE = 0 # all valves closed, blower motor off
LIFTING = 1 # lifting boat, motor on, valves open
LOWERING = 2 # lowering boat, motor off, valves open
BYPASSING = 3 # all valves open, motor off

# position of lift
LIFTED = 4
LOWERED = 5
UNKNOWN = 6

# modes
current_mode = IDLE
request_mode = None

# position
position = UNKNOWN

# push buttons
#  pins
LIFT_PIN = 18 # BCM
LOWER_PIN = 23
BYPASS_PIN = 24
STOP_PIN = 25

# push buttons
def push_button_callback(button_mode):
    request_mode = button_mode
    print ("Mode request {}".format(request_mode))

lift_buttons = Push_Buttons(push_button_callback)

lift_LEDs = LEDs()

lift_valves = Valves()

lift_motor = Blower_Motor()

def start_lifting ():
    lift_LEDs.set_lift()
    lift_Valves.lifting()
    lift_motor.on()
  


while True:

    if request_mode != None: # user requested a change
        print ("Mode requested {} are equal {}".format(request_mode,(request_mode is "LIFT")))
        if request_mode is "LIFT":
            print ("here")
            start_lifting() 
            current_mode = LIFTING

        request_mode = None

    if current_mode == LIFTING:
        lift_Valves.lifting()
            
 



