"""

determines position of the lift (height)

lift has 3 defined positions

LOWERED
LIFTED
LIFTEDMAX


"""
import RPi.GPIO as GPIO

import time

from ultrasonic_sensor import UltraSonic

LOWERED = 30
LIFTED = 90
LIFTED_MAX = 110


class Lift_Position:

    def __init__(self): # using GPIO.BOARD

        self.us_sensor = UltraSonic()

    def get(self): #returns the position of the lift

        distance = self.us_sensor.distance()

        if distance is None:
            return "ERROR UNKNOWN",None
        elif distance < LOWERED:
            return "LOWERED",distance
        elif distance > LIFTED_MAX:
            return "LIFTEDMAX",distance
        elif distance > LIFTED:
            return "LIFTED",distance
        else:
            return "BETWEENLOWEREDLIFTED",distance

    def done_lifting(self):
        position,height = self.get()
        if height is not None:
            return height > LIFTED+5
        else:
            return False

    def done_lifting_max(self):
        position,height = self.get()
        if height is not None:
            return height > LIFTED_MAX+5
        else:
            return False

    def done_lowering(self):
        position,height = self.get()
        if height is not None:
            return height < LOWERED 
        else:
            return False

    def is_lifted(self):
        return self.get() [0] =='LIFTED'

    def is_lifted_max(self):
        return self.get() [0]=='LIFTEDMAX'

    def is_lowered(self):
        return self.get() [0]=='LOWERED'

   

if __name__ == "__main__":
    
    GPIO.setmode(GPIO.BOARD)

    pbs = Lift_Position()


    while True:
        print (pbs.get())
 
        print (pbs.is_lowered())

        print (pbs.done_lowering())

        time.sleep(1)
        pass

