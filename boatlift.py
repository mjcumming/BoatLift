"""


Boat lift

GPIO Pins (BOARD)

LEDs 7,11,13,15
Buttons 32,36,38,40
Valves 29,31,33,35
Float Switches 16,18,22
Motor 37

"""



import RPi.GPIO as GPIO
import datetime
import time
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from roll_pitch import Roll_Pitch
from valves import Valves
from LEDs import LEDs
from push_buttons import Push_Buttons
from blower_motor import Blower_Motor
#from ultrasonic_sensor import UltraSonic
from lift_position import Lift_Position
from device_boatlift import Device_BoatLift



"""

Constants

"""

#request modes
LIFT = 1
LIFT_MAX = 5
LOWER = 2
BYPASS_BLOWER_OFF = 3
BYPASS_BLOWER_ON = 6
STOP = 4

# operating modes of lift
IDLE = 0 # all valves closed, blower motor off
LIFTING = 1 # lifting boat, motor on, valves open, lift to stadard position
LIFTING_MAX = 4 # lifting boat, motor on, valves open, lift all the way to top 
LOWERING = 2 # lowering boat, motor off, valves open
BYPASSING_BLOWER_OFF = 3 # all valves open, motor off
BYPASSING_BLOWER_ON = 5 # all valves open, motor off

# position of lift
LIFTED_MAX = 3
LIFTED = 1
LOWERED = 2
UNKNOWN = 0

# ultrasound distances
#HEIGHT_LOWERED = 20 #cm
#HEIGHT_RAISED = 80 #cm

ROLL_GOAL = 0
PITCH_GOAL = -2 # bow up slightly
ROLL_RANGE = 2
PITCH_RANGE = 2
ROLL_SAFETY = 10 # max roll safety
PITCH_SAFETY = 10 # max pitch before error

SAFETY_ENABLED = True # abort operation if unsafe angles


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

# timer to send updates
update_interval = 6 # seconds
last_update_time = time.time()

        
mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}


"""

Initialize

"""


GPIO.setmode(GPIO.BOARD)

def set_lift_mode(mode): # call to set the operation of the lift
    global request_mode
    request_mode = mode    

# push buttons
def push_button_callback(mode,modifier):
    logging.info ("Mode request {}, modifier {}".format(mode,modifier))

    if mode =='LIFT':
        if modifier == 'LONG':
            set_lift_mode(LIFT_MAX)
        else:
            set_lift_mode(LIFT)
    elif mode == 'LOWER':
        set_lift_mode(LOWER)
    elif mode =='BYPASS':
        if modifier == 'LONG':
            set_lift_mode(BYPASS_BLOWER_OFF)
        else:
            set_lift_mode(BYPASS_BLOWER_ON)
    elif mode == 'STOP':
        set_lift_mode (STOP)

lift_buttons = Push_Buttons(push_button_callback)

#button leds
lift_LEDs = LEDs()


#position
def lift_position_callback(pos):
    global position
    position = pos
    logging.info ('Lift postion {}'.format(position))

lift_position = Lift_Position(lift_position_callback)



#valves
lift_valves = Valves()

#blower motor
lift_motor = Blower_Motor()

#roll and pitch
lift_roll_pitch = Roll_Pitch()

#MQTT
def set_lift_mode_callback(mode):
    if mode =='LIFT':
        set_lift_mode(LIFT)
    elif mode == 'LIFTMAX':
        set_lift_mode(LIFT_MAX)
    elif mode == 'LOWER':
        set_lift_mode(LOWER)
    elif mode == 'STOP':
        set_lift_mode (STOP)

lift_mqtt = Device_BoatLift(device_id='boatlift',name = 'Boat Lift',mqtt_settings=mqtt_settings,set_lift_mode=set_lift_mode_callback)

#functions to start a mode
def start_lifting (max_lift):
    logging.info('start lifting',max_lift)
    global current_mode 
    if max_lift:
        current_mode = LIFTING_MAX
    else:
        current_mode = LIFTING
    lift_LEDs.set_lift()
    lift_motor.on()
    global mode_start_time 
    mode_start_time = time.time()
    global mode_expire_minutes
    mode_expire_minutes = 4

def start_lowering ():
    global current_mode 
    current_mode = LOWERING
    lift_LEDs.set_lower()
    lift_motor.off()  
    global mode_start_time 
    mode_start_time = time.time()
    global mode_expire_minutes
    mode_expire_minutes = 10

def start_bypassing (bloweron):
    global current_mode
    if bloweron: 
        current_mode = BYPASSING_BLOWER_ON
        lift_motor.on()  
    else:
        current_mode = BYPASSING_BLOWER_OFF
        lift_motor.off()  
    lift_LEDs.set_bypass() 
    lift_valves.set_all (True,True,True,True)
    global mode_start_time 
    mode_start_time = time.time()
    global mode_expire_minutes
    mode_expire_minutes = 10

def start_idle ():
    global mode_start_time
    mode_start_time = None
    global current_mode 
    current_mode = IDLE 
    lift_motor.off()  
    lift_valves.set_all (False,False,False,False)

    position = lift_position.get()

    #logging.info ("Lift position {}".format(position))

    if lift_position.is_lifted():
        lift_LEDs.set_lifted()
    elif lift_position.is_lifted_max():
        lift_LEDs.set_lifted_max()
    elif lift_position.is_lowered():
        lift_LEDs.set_lowered()
    else:
        lift_LEDs.set_unknown()

def start_abort():
    logging.info ('ABORTING')
    start_idle()
    lift_LEDs.set_error()

logging.info ("Starting Boat Lift")

start_idle() 

try:

    while True:

        if request_mode != None: # user requested a change
            logging.info ("Mode requested {}".format(request_mode))
            
            if request_mode == LIFT or request_mode == LIFT_MAX:
                start_lifting(request_mode == LIFT_MAX) 
            elif request_mode == LOWER:
                start_lowering() 
            elif request_mode == BYPASS_BLOWER_OFF:
                start_bypassing(False) 
            elif request_mode == BYPASS_BLOWER_ON:
                start_bypassing(True) 
            elif request_mode == STOP:
                start_idle() 

            request_mode = None

        roll,pitch = lift_roll_pitch.read()
        safe = lift_roll_pitch.check_within_parameters(ROLL_SAFETY,PITCH_SAFETY)
        position = lift_position.get()

        if SAFETY_ENABLED and not safe:
            start_abort()

        if current_mode == IDLE and safe:
            start_idle()
    
        if current_mode != IDLE or (time.time() - last_update_time) > update_interval:
            last_update_time = time.time()

            text_mode = ''
            if current_mode == IDLE:
                text_mode ='IDLE'
            elif current_mode == LIFTING:
                text_mode ='LIFTING'
            elif current_mode == LIFTING_MAX:
                text_mode ='LIFTING MAX'
            elif current_mode == LOWERING:
                text_mode ='LOWERING'

            payload = "Roll: {}  Pitch {}   Within parameters {}   Position {}    Mode {} ".format (roll,pitch, safe, position, text_mode)
            lift_mqtt.update(roll,pitch,position,text_mode)
            logging.info(payload)
            #lift_valves.logging.info()

        if current_mode == LIFTING or current_mode == LIFTING_MAX:
            lift_valves.lifting(roll,pitch,ROLL_GOAL,PITCH_GOAL,ROLL_RANGE,PITCH_RANGE)

            if (current_mode == LIFTING and (lift_position.is_lifted() or lift_position.is_lifted_max())) or (current_mode == LIFTING_MAX and lift_position.is_lifted_max()):
                start_idle() 

        elif current_mode == LOWERING:
            lift_valves.lowering(roll,pitch,ROLL_GOAL,PITCH_GOAL,ROLL_RANGE,PITCH_RANGE)

            if lift_position.is_lowered():
                start_idle() 

        elif current_mode == BYPASSING_BLOWER_OFF or current_mode == BYPASSING_BLOWER_ON: # NOT WORKING
            safe = lift_roll_pitch.check_within_parameters(ROLL_SAFETY,PITCH_SAFETY)
            
        # check how long we have been running
        if mode_start_time != None:
            elapsed_time = time.time() - mode_start_time
            #logging.info ('Elapsed Time: {}'.format(elapsed_time))

            if elapsed_time > mode_expire_minutes*60: 
                logging.info ("Watch dog time expired")
                start_idle()

        time.sleep (.5)

except KeyboardInterrupt:
    logging.info("Stopped by User")
    GPIO.cleanup()

