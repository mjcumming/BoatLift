"""


Boat lift

GPIO Pins (BOARD)

LEDs 11,13,15
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
from lift_position_ultrasound import Lift_Position
from device_boatlift import Device_BoatLift
from ds18b20 import DS18B20


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
LEVEL = 7

# operating modes of lift
IDLE = 0 # all valves closed, blower motor off
LIFTING = 1 # lifting boat, motor on, valves open, lift to stadard position
LIFTING_MAX = 4 # lifting boat, motor on, valves open, lift all the way to top 
LOWERING = 2 # lowering boat, motor off, valves open
BYPASSING_BLOWER_OFF = 3 # all valves open, motor off
BYPASSING_BLOWER_ON = 5 # all valves open, motor off
LEVELING = 6

# position of lift
LIFTED_MAX = 3
LIFTED = 1
LOWERED = 2
UNKNOWN = 0

# ultrasound distances
#HEIGHT_LOWERED = 20 #cm
#HEIGHT_RAISED = 80 #cm

ROLL_GOAL = 0
PITCH_GOAL = -0.5 # bow up slightly
LOWERING_ROLL_RANGE = 2 
LOWERING_PITCH_RANGE = 2
LIFTING_ROLL_RANGE = 1.5
LIFTING_PITCH_RANGE = 1.5
LEVELING_ROLL_RANGE = .5
LEVELING_PITCH_RANGE = .5
ROLL_SAFETY = 10 # max roll safety
PITCH_SAFETY = 10 # max pitch before error


SAFETY_ENABLED = True # abort operation if unsafe angles


"""

Globals


"""

# modes
current_mode = IDLE
prev_mode = IDLE
request_mode = None

mode_start_time = None
mode_expire_minutes = None

# position
#position = 0
#last_position = -1

lift_height = 0
last_lift_height = -1

# timer to send updates
update_interval = 900 # seconds, 15minutes
last_update_time = None

        
mqtt_settings = {
    'MQTT_BROKER' : 'openhabianpi.local',
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
    logger.info ("Mode request {}, modifier {}".format(mode,modifier))

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
'''
def lift_position_callback(pos):
    global position
    position = pos
    logger.info ('Lift postion {}'.format(position))

lift_position = Lift_Position(lift_position_callback)
prev_lift_position = lift_position.get()
'''

#valves
lift_valves = Valves()

#blower motor
lift_motor = Blower_Motor()

#roll and pitch
lift_roll_pitch = Roll_Pitch()
prev_roll = 0
prev_pitch = 0

#water temp
try:
    water_temp = DS18B20()
except Exception as ex:
    water_temp = None
    logger.warn('DS TEMPERATURE ERROR: {}'.format(ex))

prev_water_temperature = 0


#MQTT
def set_lift_mode_callback(mode):
    if mode =='LIFT':
        set_lift_mode(LIFT)
    elif mode == 'LIFTMAX':
        set_lift_mode(LIFT_MAX)
    elif mode == 'LEVEL':
        set_lift_mode(LEVEL)
    elif mode == 'LOWER':
        set_lift_mode(LOWER)
    elif mode == 'STOP':
        set_lift_mode (STOP)
    elif mode == 'BYPASS_BLOWER_OFF':
        set_lift_mode (BYPASS_BLOWER_OFF)
    elif mode == 'BYPASS_BLOWER_ON':
        set_lift_mode (BYPASS_BLOWER_ON)

lift_mqtt = Device_BoatLift(device_id='boatlift',name = 'Boat Lift',mqtt_settings=mqtt_settings,set_lift_mode=set_lift_mode_callback)

#functions to start a mode
def start_lifting (max_lift):
    global current_mode 
    if max_lift:
        current_mode = LIFTING_MAX
    else:
        current_mode = LIFTING
    logger.info('start lifting mode {}'.format(current_mode))
    #print('!!!!!!!!!!!!!!!!!!!!!!!!!start lifting mode {}'.format(current_mode))
    lift_LEDs.set_lift()
    lift_motor.on()
    global mode_start_time 
    mode_start_time = time.time()
    global mode_expire_minutes
    mode_expire_minutes = 4

#functions to start a mode
def start_leveling ():
    global current_mode 
    current_mode = LIFTING
    logger.info('start leveling mode {}'.format(current_mode))

    lift_motor.on()
    global mode_start_time 
    mode_start_time = time.time()
    global mode_expire_minutes
    mode_expire_minutes = .5

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

    if current_mode == LOWERING:
        lift_valves.set_all (True,True,True,True) # keep valves open
    else:
        lift_valves.set_all (False,False,False,False)

    current_mode = IDLE 
    lift_motor.off()  

    #logger.info ("Lift position {}".format(position))

    if lift_position.is_lifted():
        lift_LEDs.set_lifted()
    elif lift_position.is_lifted_max():
        lift_LEDs.set_lifted_max()
    elif lift_position.is_lowered():
        lift_LEDs.set_lowered()
    else:
        lift_LEDs.set_unknown()

def start_abort():
    logger.info ('ABORTING')
    start_idle()
    lift_LEDs.set_error()

logger.info ("Starting Boat Lift")

start_idle() 

try:

    while True:

        if request_mode != None: # user requested a change
            logger.info ("Mode requested {}".format(request_mode))
            
            if request_mode == LIFT or request_mode == LIFT_MAX:
                start_lifting(request_mode == LIFT_MAX) 
            elif request_mode == LEVEL:
                start_leveling() 
            elif request_mode == LOWER:
                start_lowering() 
            elif request_mode == BYPASS_BLOWER_OFF:
                start_bypassing(False) 
            elif request_mode == BYPASS_BLOWER_ON:
                start_bypassing(True) 
            elif request_mode == STOP:
                start_idle() 

            request_mode = None

        safe = lift_roll_pitch.check_within_parameters(ROLL_SAFETY,PITCH_SAFETY)

        if SAFETY_ENABLED and not safe:
            start_abort()

        #? not sure why
        #if current_mode == IDLE and safe:
        #    start_idle()

        water_temperature = 0
        if water_temp is not None:
            water_temperature=round(water_temp.get_temperature(),1)

        roll,pitch = lift_roll_pitch.read_average()
        lift_position,lift_height = lift_position.get() 

        send_resting_update = False

        if (prev_water_temperature - 0.5) < water_temperature < (prev_water_temperature + 0.5) is False:
            send_resting_update = True
    
        if (prev_roll - 0.5) < roll < (prev_roll + 0.5) is False:
            send_resting_update = True
    
        if (prev_pitch - 0.5) < pitch < (prev_pitch + 0.5) is False:
            send_resting_update = True
    
#        if prev_lift_position != position:
#            send_resting_update = True

        if (lift_height - 5) < lift_height < (lift_height + 5):
            send_resting_update = True

        if prev_mode != current_mode:
            send_resting_update = True
    
        if last_update_time is None or (time.time() - last_update_time) > update_interval:
            send_resting_update = True

        prev_roll = roll
        prev_pitch = pitch
        prev_lift_position = position
        prev_water_temperature = water_temperature
        prev_mode = current_mode

        if current_mode != IDLE or send_resting_update:
            last_update_time = time.time()

            text_mode = ''
            if current_mode == IDLE:
                text_mode ='IDLE'
            elif current_mode == LIFTING:
                text_mode ='LIFTING'
            elif current_mode == LIFTING_MAX:
                text_mode ='LIFTING MAX'
            elif current_mode == LEVELING:
                text_mode ='LEVELING'
            elif current_mode == LOWERING:
                text_mode ='LOWERING'
            elif current_mode == BYPASSING_BLOWER_OFF:
                text_mode ='BYPASSING BLOWER OFF'
            elif current_mode == BYPASSING_BLOWER_ON:
                text_mode ='BYPASSING BLOWER ON'

            valve_positions = lift_valves.get_text()
            
            elapsed_time = "{}".format(time.time() - mode_start_time)
            lift_mqtt.update(roll,pitch,lift_position,lift_height,text_mode,valve_positions,water_temperature,elapsed_time)
            
            logger.info("Roll: {}  Pitch {}   Within parameters {}   Position {}  Valves {}  Mode {} Time {}".format (roll,pitch, safe, position, valve_positions, text_mode, elapsed_time))

        if current_mode == LIFTING or current_mode == LIFTING_MAX:
            lift_valves.lifting(roll,pitch,ROLL_GOAL,PITCH_GOAL,LIFTING_ROLL_RANGE,LIFTING_PITCH_RANGE)

            if current_mode == LIFTING and lift_position.is_lifted():
                #start_leveling()
                start_idle()
            elif lift_position.is_lifted() or lift_position.is_lifted_max():
                start_idle() 

        elif current_mode == LEVELING:
            lift_valves.lifting(roll,pitch,ROLL_GOAL,PITCH_GOAL,LEVELING_ROLL_RANGE,LEVELING_PITCH_RANGE)

            if (ROLL_GOAL-LEVELING_ROLL_RANGE) < roll < (ROLL_GOAL-LEVELING_ROLL_RANGE):
                if (PITCH_GOAL-LEVELING_PITCH_RANGE) < pitch < (PITCH_GOAL-LEVELING_PITCH_RANGE):
                    start_idle()

        elif current_mode == LOWERING:
            lift_valves.lowering(roll,pitch,ROLL_GOAL,PITCH_GOAL,LOWERING_ROLL_RANGE,LOWERING_PITCH_RANGE)

            if lift_position.is_lowered():
                start_idle() 

        elif current_mode == BYPASSING_BLOWER_OFF or current_mode == BYPASSING_BLOWER_ON: # NOT WORKING
            pass
            #safe = lift_roll_pitch.check_within_parameters(ROLL_SAFETY,PITCH_SAFETY)
            
        # check how long we have been running
        if mode_start_time != None:
            elapsed_time = time.time() - mode_start_time
            #logger.info ('Elapsed Time: {}'.format(elapsed_time))

            if elapsed_time > mode_expire_minutes*60: 
                logger.info ("Watch dog time expired")
                start_idle()

        time.sleep (1)

except KeyboardInterrupt:
    logger.info("Stopped by User")
    GPIO.cleanup()

