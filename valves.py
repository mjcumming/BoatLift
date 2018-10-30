 
import RPi.GPIO as GPIO

import time

from valve import Valve

valve_list = {
    "bow_startboard" : 29,  #BOARD
    "bow_port" : 31,
    "stern_startboard" : 33,
    "stern_port" : 35,
}

class Valves:

    list = {}

    def __init__(self): # using GPIO.BOARD
        for name,bcm in valve_list.items():
            self.list [name] = Valve (name,bcm)
    
    def open_all (self):
        for name,valve in self.list.items():
            valve.open()

    def close_all (self):
        for name,valve in self.list.items():
            valve.close()

    def set_all (self, bs, bp, ss, sp):
        self.list ["bow_starboard"].set (bs)
        self.list ["bow_port"].set (bs)
        self.list ["stern_starboard"].set (bs)
        self.list ["stern_port"].set (bs)

    def lifting(self,roll,pitch,roll_goal, pitch_goal, roll_range, pitch_range):
        # assume all tanks should be off
        bp = False
        bs = False
        sp = False
        ss = False
        
        if roll > (roll_goal + roll_range): # leaning to starboard
            bp = True
            sp = True

        elif roll < (roll_goal - roll_range): # leaning to port
            bs = True
            ss = True

        if pitch > (pitch_goal + pitch_range): # leaning to bow
            bs = True
            bs = True

        elif pitch < (pitch_goal - pitch_range): # leaning to stern
            ss = True
            sp = True

        self.set_all (bp,bs,sp,ss)

    def lowering(self,roll,pitch,roll_goal, pitch_goal, roll_range, pitch_range):
 
        # assume all tanks should be on
        bp = True
        bs = True
        sp = True
        ss = True
        
        if roll > (roll_goal + roll_range): # leaning to starboard
            bs = False
            ss = False

        elif roll < (roll_goal - roll_range): # leaning to port
            bs = False
            ss = False

        if pitch > (pitch_goal + pitch_range): # leaning to bow
            bs = False
            bs = False

        elif pitch < (pitch_goal - pitch_range): # leaning to stern
            ss = False
            sp = False

        self.set_all (bp,bs,sp,ss)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    valves = Valves ()
 
    while True:
        valves.open_all()
        time.sleep (1)

        valves.close_all()
        time.sleep (1)