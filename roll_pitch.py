"""

roll + = tilting starboard 

pitch + = tilting to bow




"""
import logging
logger = logging.getLogger(__name__)

from inclinometer import Inclinometer

import time

from statistics import mean 

pitch_correction = 3.5
roll_correction = -7.7


class Roll_Pitch:
    MAX_UNSAFE_CONSEQ_READS = 3 # number of safety reads before error
    
    last_check_not_safe = 0 # number of consecutive unsafe measurements before error
    roll = None
    pitch = None


    def __init__(self):

        success = False

        self.roll_values = list()
        self.pitch_values = list ()

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

    def read_average(self):
        roll,pitch = self.read()
        self.roll_values.append (roll)
        self.pitch_values.append (pitch)

        if len(self.roll_values) > 20:
            self.roll_values.pop(0)
        if len(self.pitch_values) > 20:
            self.pitch_values.pop(0)

        return round(mean(self.roll_values),1),round(mean(self.pitch_values),1)

    def check_within_parameters(self,roll_safety, pitch_safety):
        roll,pitch = self.read_average()
        if roll > roll_safety or roll < -roll_safety or pitch > pitch_safety or pitch < -pitch_safety:
            self.last_check_not_safe += 1

            if self.last_check_not_safe > self.MAX_UNSAFE_CONSEQ_READS: # already one ba
                return False
        else: 
            self.last_check_not_safe = 0
            
        return True


                 
if __name__ == "__main__":
    rp = Roll_Pitch ()
 
    while True:
        roll,pitch = rp.read_average()
        logging.info("Roll: {}  Pitch {}   Within parameters {}".format (roll,pitch, rp.check_within_parameters(10,10)))
        print("Roll: {}  Pitch {}   Within parameters {}".format (roll,pitch, rp.check_within_parameters(10,10)))
        time.sleep (.5)
