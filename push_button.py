

import RPi.GPIO as GPIO

import time

LONGPRESS = 2 # seconds

class Push_Button:
    
    pin = None # BOARD
    name = None

    def __init__(self, name, pin, callback): # using GPIO.BOARD
        self.pin = pin
        self.name = name
        self.callback = callback
        self.start_time = None

        def button_callback(channel):
            #print ('button callback',channel, GPIO.input(channel))
            
            if GPIO.input(channel) == 0:
                self.start_time = time.time()
            elif self.start_time:
                elapsed_time = time.time() - self.start_time
                self.start_time = None
                #print ('elapsed',elapsed_time)
                if elapsed_time > LONGPRESS:
                    self.callback(self.name,'LONG')
                else:
                    self.callback(self.name,'SHORT')
            
        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled low (off)
 
        GPIO.add_event_detect(self.pin,GPIO.BOTH,callback=button_callback, bouncetime=100) # Setup event on pin rising edge

    

if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)
    def callback (result,duration):
        print ("Button Pushed: {}  {}".format(result,duration))

    pbs = Push_Button('Lift',19,callback)
    while True:
        pass  