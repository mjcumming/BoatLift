#!/usr/bin/env python
import time

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_enum import Property_Enum
from homie.node.property.property_string import Property_String


LIFT_MODES = ['LIFT','LIFTMAX','LOWER','STOP']


class Device_BoatLift(Device_Base):


    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None, set_lift_mode=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        self.set_lift_mode=set_lift_mode

        node = (Node_Base(self,'boatlift','Boat Lift','boatlift'))
        self.add_node (node)

        self.lift_mode = Property_Enum (node,id='liftmode',name='Lift Mode',data_format=','.join(LIFT_MODES),set_value = lambda value: self.set_lift_mode(value) )
        node.add_property (self.lift_mode)

        self.lift_position = Property_String (node,id='liftposition',name='Lift Position')
        node.add_property (self.lift_position)

        self.lift_roll = Property_String (node,id='liftroll',name='Lift Roll')
        node.add_property (self.lift_roll)

        self.lift_pitch = Property_String (node,id='liftpitch',name='Lift Pitch')
        node.add_property (self.lift_pitch)

        self.start()

    def update(self,roll,pitch,position,mode):
        self.lift_roll.value = roll
        self.lift_pitch.value = pitch
        self.lift_position.value = position
        self.lift_mode.value = mode
        
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
