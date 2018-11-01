"""


Boat lift

GPIO Pins (BOARD)

LEDs 7,11,13,15
Buttons 22,32,36,38
Valves 29,31,33,35
Ultrasound 37,40
Motor 18

"""


import RPi.GPIO as GPIO
import datetime
import time

from roll_pitch import Roll_Pitch
from valves import Valves
from LEDs import LEDs
from push_buttons import Push_Buttons
from blower_motor import Blower_Motor
from ultrasonic_sensor import UltraSonic


"""

Constants

"""

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
LIFTED = 1
LOWERED = 2
UNKNOWN = 0

# ultrasound distances
HEIGHT_LOWERED = 20 #cm
HEIGHT_RAISED = 80 #cm

ROLL_GOAL = 0
PITCH_GOAL = 2
ROLL_RANGE = 3
PITCH_RANGE = 3
ROLL_SAFETY = 10 # max roll safety
PITCH_SAFETY = 10 # max pitch before error

"""

Globals


"""

# modes
current_mode = IDLE
request_mode = None

mode_start_time = None
mode_expire_minutes = None

# position
position = UNKNOWN

"""

Initialize

"""


GPIO.setmode(GPIO.BOARD)


# push buttons
def push_button_callback(button_mode):
    global request_mode
    request_mode = button_mode
    print ("Mode request {}".format(request_mode))

lift_buttons = Push_Buttons(push_button_callback)

lift_LEDs = LEDs()

lift_valves = Valves()

lift_motor = Blower_Motor()

lift_roll_pitch = Roll_Pitch()

lift_height = UltraSonic()


def start_lifting ():
    global current_mode 
    current_mode = LIFTING
    lift_LEDs.set_lift()
    lift_motor.on()
    global mode_start_time 
    mode_start_time = datetime.datetime.now()
    global mode_expire_minutes
    mode_expire_minutes = 4

def start_lowering ():
    global current_mode 
    current_mode = LOWERING
    lift_LEDs.set_lower()
    lift_motor.off()  
    global mode_start_time 
    mode_start_time = datetime.datetime.now()
    global mode_expire_minutes
    mode_expire_minutes = 10

def start_bypassing ():
    global current_mode 
    current_mode = BYPASSING
    lift_LEDs.set_bypass()
    lift_motor.off()  
    lift_valves.set_all (True,True,True,True)
    global mode_start_time 
    mode_start_time = datetime.datetime.now()
    global mode_expire_minutes
    mode_expire_minutes = 10

def start_idle ():
    global mode_start_time
    mode_start_time = None
    global current_mode 
    current_mode = IDLE 
    lift_motor.off()  
    lift_valves.set_all (False,False,False,False)

    height = lift_height.distance()

    if height and height > HEIGHT_RAISED:
        position = LIFTED
    elif height < HEIGHT_LOWERED:
        position = LOWERED
    else:
        position = UNKNOWN

    print ("Lift position {}  Height {}".format(position,height))

    if position == UNKNOWN:
        lift_LEDs.set_unknown()
    elif position == LIFTED:
        lift_LEDs.set_lifted()
    elif position == LOWERED:
        lift_LEDs.set_lowered()

print ("Starting")

start_idle() 

try:

    while True:

        if request_mode != None: # user requested a change
            print ("Mode requested {}".format(request_mode))
            
            if request_mode is "LIFT":
                start_lifting() 
            elif request_mode is "LOWER":
                start_lowering() 
            elif request_mode is "BYPASS":
                start_bypassing() 
            elif request_mode is "STOP":
                start_idle() 

            request_mode = None

        if current_mode == LIFTING:
            roll,pitch = lift_roll_pitch.read()
            lift_valves.lifting(roll,pitch,ROLL_GOAL,PITCH_GOAL,ROLL_RANGE,PITCH_RANGE)
            safe = lift_roll_pitch.check_within_parameters(ROLL_SAFETY,PITCH_SAFETY)

            height = lift_height.distance()

            if height and height > HEIGHT_RAISED:
                position = LIFTED
                start_idle() 

            print("Roll: {}  Pitch {}   Within parameters {}   Height {}".format (roll,pitch, safe, height))
    
        elif current_mode == LOWERING:
            roll,pitch = lift_roll_pitch.read()
            lift_valves.lowering(roll,pitch,ROLL_GOAL,PITCH_GOAL,ROLL_RANGE,PITCH_RANGE)
            safe = lift_roll_pitch.check_within_parameters(ROLL_SAFETY,PITCH_SAFETY)

            height = lift_height.distance()
            
            if height and height < HEIGHT_LOWERED:
                position = LOWERED
                start_idle() 

            print("Roll: {}  Pitch {}   Within parameters {}   Height {}".format (roll,pitch, safe, height))

        elif current_mode == BYPASSING:
            roll,pitch = lift_roll_pitch.read()
            lift_valves.lowering(roll,pitch,ROLL_GOAL,PITCH_GOAL,ROLL_RANGE,PITCH_RANGE)
            safe = lift_roll_pitch.check_within_parameters(ROLL_SAFETY,PITCH_SAFETY)

            height = lift_height.distance()
            
            print("Roll: {}  Pitch {}   Within parameters {}   Height {}".format (roll,pitch, safe, height))
    
        # check how long we have been running
        if mode_start_time != None:
            if (datetime.datetime.now() - mode_start_time).seconds > mode_expire_minutes*60: 
                print ("Watch dog time expired")
                position = UNKNOWN
                start_idle()

        time.sleep (1)

except KeyboardInterrupt:
    print("Stopped by User")
    GPIO.cleanup()

