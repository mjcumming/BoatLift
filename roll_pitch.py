"""
"""


from inclinometer import Inclinometer

import time


class Roll_Pitch:

    ROLL_SAFETY = 10 # max roll safety

    PITCH_SAFETY = 10 # max pitch before error

    MAX_UNSAFE_CONSEQ_READS = 3 # number of safety reads before error
    
    last_check_not_safe = 0 # number of consecutive unsafe measurements before error
    roll = None
    pitche = None


    def __init__(self):
        self.inclinometer = Inclinometer()

    
    def read(self): # return so that roll/pitch are 0 when level, + numbers = leaning to starboard or bow
        self.roll,self.pitch = self.inclinometer.get_angles()
        return self.roll,self.pitch

    def check_within_parameters(self):
        if self.roll > 10 or self.roll < 10 or self.pitch > 10 or self.pitch < 10:
            self.last_check_not_safe += 1

            if self.last_check_not_safe > self.MAX_UNSAFE_CONSEQ_READS: # already one ba
                return False
        else: 
            self.last_check_not_safe = 0
            
        return True


                 
if __name__ == "__main__":
    rp = Roll_Pitch ()
 
    while True:
        roll,pitch = rp.read()
        print("Roll: {}  Pitch {}   Within parameters {}".format (roll,pitch, rp.check_within_parameters()))
        time.sleep (1)
