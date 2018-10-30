"""


Boat lift


"""


import RPi.GPIO as GPIO
import time

from roll_pitch import Roll_Pitch
from valves import Valves
from LEDs import LEDs
from push_buttons import Push_Buttons

GPIO.setmode(GPIO.BOARD)



# operating modes of lift
IDLE = 0 # all valves closed, blower motor off
LIFTING = 1 # lifting boat, motor on, valves open
LOWERING = 2 # lowering boat, motor off, valves open
BYPASS = 3 # all valves open, motor off

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
def push_button_callback(button_mode)
    request_mode = button_mode

lift_buttons = Push_Buttons(push_button_callback)

while True:

    inc.get_angles()
    time.sleep (1)

