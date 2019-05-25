"""

roll + = tilting port 

pitch + = tilting to bow




"""
import logging
logger = logging.getLogger(__name__)

from inclinometer import Inclinometer

import time

pitch_correction = 2
roll_correction = 4


class Roll_Pitch:
    MAX_UNSAFE_CONSEQ_READS = 3 # number of safety reads before error
    
    last_check_not_safe = 0 # number of consecutive unsafe measurements before error
    roll = None
    pitch = None


    def __init__(self):

        success = False

        while success is False:
            try:
                self.inclinometer = Inclinometer()
                success = True
            except IOError:
                logging.error ('mpu 6050 IO error')
                time.sleep(1)
    
    def read(self): # return so that roll/pitch are 0 when level, + numbers = leaning to starboard or bow
        x,y = self.inclinometer.get_angles() # as setup, the inclinometer does not ever return a pitch of 180 - not why. so we never get a pitch of 0 if we use 180 instead of 179
        if x > 0:
            x = 179 - x
        else:
            x = abs(x) - 180
    
        self.roll = y+roll_correction
        self.pitch = x+pitch_correction
        return self.roll,self.pitch

    def check_within_parameters(self,roll_safety, pitch_safety):
        if self.roll > roll_safety or self.roll < -roll_safety or self.pitch > pitch_safety or self.pitch < -pitch_safety:
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
        logging.info("Roll: {}  Pitch {}   Within parameters {}".format (roll,pitch, rp.check_within_parameters(10,10)))
        print("Roll: {}  Pitch {}   Within parameters {}".format (roll,pitch, rp.check_within_parameters(10,10)))
        time.sleep (.5)
