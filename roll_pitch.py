"""

roll + = tilting port 

pitch + = tilting to stern




"""


from inclinometer import Inclinometer

import time


class Roll_Pitch:
    MAX_UNSAFE_CONSEQ_READS = 3 # number of safety reads before error
    
    last_check_not_safe = 0 # number of consecutive unsafe measurements before error
    roll = None
    pitche = None


    def __init__(self):
        self.inclinometer = Inclinometer()

    
    def read(self): # return so that roll/pitch are 0 when level, + numbers = leaning to starboard or bow
        x,y = self.inclinometer.get_angles()
        if x > 0:
            x = 180 - x
        else:
            x = abs(x) - 180
    
        self.roll,self.pitch = y,x
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
        print("Roll: {}  Pitch {}   Within parameters {}".format (roll,pitch, rp.check_within_parameters()))
        time.sleep (1)
