#!/usr/bin/env python
import time

import homie
from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_enum import Property_Enum
from homie.node.property.property_string import Property_String
from homie.node.property.property_temperature import Property_Temperature


LIFT_MODES = ['LIFT','LIFTMAX','LOWER','STOP','BYPASS_BLOWER_ON','BYPASS_BLOWER_OFF']


class Device_BoatLift(Device_Base):


    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None, set_lift_mode=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base(self,'boatlift','Boat Lift','boatlift'))
        self.add_node (node)

        self.set_lift_mode = Property_Enum (node,id='setliftmode',name='Set Lift Mode',data_format=','.join(LIFT_MODES),set_value = lambda value: set_lift_mode(value) )
        node.add_property (self.set_lift_mode)

        self.lift_mode = Property_String (node,id='liftmode',name='Lift Mode')
        node.add_property (self.lift_mode)

        self.lift_position = Property_String (node,id='position',name='Position')
        node.add_property (self.lift_position)

        self.lift_roll = Property_String (node,id='roll',name='Roll')
        node.add_property (self.lift_roll)

        self.lift_pitch = Property_String (node,id='pitch',name='Pitch')
        node.add_property (self.lift_pitch)

        self.valves = Property_String (node,id='valves',name='Valves')
        node.add_property (self.valves)

        self.water_temp = Property_Temperature (node,id='watertemp',name='Water Temp',unit='C')
        node.add_property (self.water_temp)

        self.start()

    def update(self,roll,pitch,position,mode,valves,water_temp):
        self.lift_roll.value = roll
        self.lift_pitch.value = pitch
        self.lift_position.value = position
        self.lift_mode.value = mode
        self.valves.value = valves
        self.water_temp.value = water_temp
        
mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}


if __name__ == '__main__':
    try:
        
        boatlift = Device_BoatLift (name = 'Boat Lift',mqtt_settings=mqtt_settings)

        while True:
            time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        
