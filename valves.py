 
import RPi.GPIO as GPIO

import time

from valve import Valve

valve_list = {
    "bow_starboard" : 29,  #BOARD
    "bow_port" : 31,
    "stern_starboard" : 33,
    "stern_port" : 35,
}

"""
roll + = tilting port 

pitch + = tilting to stern
"""


class Valves:

    list = {}

    def __init__(self): # using GPIO.BOARD
        for name,bcm in valve_list.items():
            self.list [name] = Valve (name,bcm)
    '''
    def print(self):
        print('   ^')
        print(' {}   {}'.format(self.list ["bow_port"].get() == True and '*' or '-',self.list ["bow_starboard"].get() == True and '*' or '-'))
        print(' {}   {}'.format(self.list ["stern_port"].get() == True and '*' or '-',self.list ["stern_starboard"].get() == True and '*' or '-'))
    '''  

    def open_all (self):
        for _,valve in self.list.items():
            valve.open()

    def close_all (self):
        for _,valve in self.list.items():
            valve.close()

    def set_all (self, bs, bp, ss, sp):
        #print ("Valves: Bow Starboard: {}  Bow Port: {}  Stern Starboard: {}  Stern Port: {}".format (bs,bp,ss,sp))
        self.list ["bow_starboard"].set(bs)
        self.list ["bow_port"].set(bp)
        self.list ["stern_starboard"].set(ss)
        self.list ["stern_port"].set(sp)
    
    def get_all (self):
        return self.list ["bow_starboard"].get(),self.list ["bow_port"].get(),self.list ["stern_starboard"].get(),self.list ["stern_port"].get()

    def get_text (self):
        return 'BP {}  BS {}  SP {}  SS {}'.format(self.list ["bow_port"].get() == True and '*' or '-',self.list ["bow_starboard"].get() == True and '*' or '-',self.list ["stern_port"].get() == True and '*' or '-',self.list ["stern_starboard"].get() == True and '*' or '-')

    def set_valve(self,valve,open):
        self.list[valve].set(open)

    def get_valve(self,valve):
        return self.list[valve].get()

    def lowering(self,roll,pitch,roll_goal, pitch_goal, roll_range, pitch_range):
        starboard_limit = roll_goal + roll_range
        port_limit = roll_goal - roll_range

        bow_limit = pitch_goal + pitch_range
        stern_limit = pitch_goal - pitch_range

        #bow starboard
        if roll < port_limit or pitch < stern_limit: # tilting beyond limit to port or stern
            self.set_valve('bow_starboard',True)
        elif roll > starboard_limit or pitch > bow_limit: 
            self.set_valve('bow_starboard',False)
        elif not self.get_valve("bow_starboard") and (roll <= roll_goal and pitch <= pitch_goal):
            self.set_valve('bow_starboard',True)
        else:
            self.set_valve('bow_starboard',True)

        #bow port
        if roll > starboard_limit or pitch < stern_limit: 
            self.set_valve('bow_port',True)
        elif roll < port_limit or pitch > bow_limit: 
            self.set_valve('bow_port',False)
        elif not self.get_valve("bow_port") and (roll >= roll_goal and pitch <= pitch_goal):
            self.set_valve('bow_port',True)
        else:
            self.set_valve('bow_port',True)   
                    
        #stern starboard
        if roll < port_limit or pitch > bow_limit: 
            self.set_valve('stern_starboard',True)
        elif roll > starboard_limit or pitch < stern_limit: 
            self.set_valve('stern_starboard',False)
        elif not self.get_valve("stern_starboard") and (roll <= roll_goal and pitch >= pitch_goal):
            self.set_valve('stern_starboard',True)
        else:
            self.set_valve('stern_starboard',True)

        #stern port
        if roll > starboard_limit or pitch > bow_limit: 
            self.set_valve('stern_port',True)
        elif roll < port_limit or pitch < stern_limit: 
            self.set_valve('stern_port',False)
        elif not self.get_valve("stern_port") and (roll >= roll_goal and pitch >= pitch_goal):
            self.set_valve('stern_port',True)
        else:
            self.set_valve('stern_port',True)

 
    def lifting(self,roll,pitch,roll_goal, pitch_goal, roll_range, pitch_range): # roll/pitch are 0 when level, + numbers = leaning to starboard or bow
        starboard_limit = roll_goal + roll_range
        port_limit = roll_goal - roll_range

        bow_limit = pitch_goal + pitch_range
        stern_limit = pitch_goal - pitch_range

        #bow starboard
        if roll < port_limit or pitch < stern_limit: # tilting beyond limit to port or stern
            self.set_valve('bow_starboard',False)
        elif roll > starboard_limit or pitch > bow_limit: 
            self.set_valve('bow_starboard',True)
        elif not self.get_valve("bow_starboard") and (roll >= roll_goal and pitch >= pitch_goal):
            self.set_valve('bow_starboard',True)
        else:
            self.set_valve('bow_starboard',True)

        #bow port
        if roll > starboard_limit or pitch < stern_limit: 
            self.set_valve('bow_port',False)
        elif roll < port_limit or pitch > bow_limit: 
            self.set_valve('bow_port',True)
        elif not self.get_valve("bow_port") and (roll <= roll_goal and pitch >= pitch_goal):
            self.set_valve('bow_port',True)
        else:
            self.set_valve('bow_port',True)   
                    
        #stern starboard
        if roll < port_limit or pitch > bow_limit: 
            self.set_valve('stern_starboard',False)
        elif roll > starboard_limit or pitch < stern_limit: 
            self.set_valve('stern_starboard',True)
        elif not self.get_valve("stern_starboard") and (roll >= roll_goal and pitch <= pitch_goal):
            self.set_valve('stern_starboard',True)
        else:
            self.set_valve('stern_starboard',True)

        #stern port
        if roll > starboard_limit or pitch > bow_limit: 
            self.set_valve('stern_port',False)
        elif roll < port_limit or pitch < stern_limit: 
            self.set_valve('stern_port',True)
        elif not self.get_valve("stern_port") and (roll <= roll_goal and pitch <= pitch_goal):
            self.set_valve('stern_port',True)
        else:
            self.set_valve('stern_port',True)

        print (roll,pitch,starboard_limit,port_limit,bow_limit,stern_limit)
        print(self.get_text())
 


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    valves = Valves ()
    valves.open_all()
'''

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    valves = Valves ()
    valves.close_all()
    valves.print()

    valves.lifting(0,0,0,0,3,3)
    valves.print()
    valves.lifting(0,5,0,0,3,3) # leaning to bow
    valves.print()
    valves.lifting(0,-5,0,0,3,3) # leaning stern
    valves.print()
    valves.lifting(5,0,0,0,3,3) # leaning starboard
    valves.print()
    valves.lifting(-5,0,0,0,3,3) # leaning port
    valves.print()
    valves.lifting(-5,-5,0,0,3,3) # leaning port and stern
    valves.print()
    valves.lifting(-5,5,0,0,3,3) #leaning port and bow
    valves.print()
    valves.lifting(5,5,0,0,3,3) #leaning starboard and bow
    valves.print()
    valves.lifting(5,-5,0,0,3,3) #leaning starboard and stern
    valves.print()
    valves.lifting(1,-1,0,0,3,3) #leaning starboard and stern
    valves.print()
    valves.lifting(0,0,0,0,3,3) #leaning starboard and stern
    valves.print()

    valves.lowering(0,0,0,0,3,3)
    valves.print()
    valves.lowering(0,5,0,0,3,3) # leaning to bow
    valves.print()
    valves.lowering(0,-5,0,0,3,3) # leaning stern
    valves.print()
    valves.lowering(5,0,0,0,3,3) # leaning starboard
    valves.print()
    valves.lowering(-5,0,0,0,3,3) # leaning port
    valves.print()
    valves.lowering(-5,-5,0,0,3,3) # leaning port and stern
    valves.print()
    valves.lowering(-5,5,0,0,3,3) #leaning port and bow
    valves.print()
    valves.lowering(5,5,0,0,3,3) #leaning starboard and bow
    valves.print()
    valves.lowering(5,-5,0,0,3,3) #leaning starboard and stern
    valves.print()
    valves.lowering(1,-1,0,0,3,3) #leaning starboard and stern
    valves.print()
    valves.lowering(0,0,0,0,3,3) #leaning starboard and stern
    valves.print()
    while True:
        valves.open_all()
        time.sleep (5)

        valves.close_all()
        time.sleep (5)
'''