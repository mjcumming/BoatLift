"""

Boat lift


"""


import RPi.GPIO as GPIO
import time

from roll_pitch import Roll_Pitch
from valves import Valves
from LEDs import LEDs


GPIO.setmode(GPIO.BCM)



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

# push buttons
#  pins
LIFT_PIN = 18 # BCM
LOWER_PIN = 23
BYPASS_PIN = 24
STOP_PIN = 25
#  callbacks

def lift_callback():
    request_mode = LIFTING

def lower_callback():
    request_mode = LOWERING

def bypass_callback():
    request_mode = BYPASS

def stop_callback():
    request_mode = IDLE

lift_button = Push_Button (LIFTPIN, lift_callback)

while True:

    inc.get_angles()
    time.sleep (1)

