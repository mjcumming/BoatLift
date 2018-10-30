 
import RPi.GPIO as GPIO

import time


class LED:
    
    pin = None

    PWM = None 

    def __init__(self, pin): # using GPIO.BOARD
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT) 
        self.PWM = GPIO.PWM(self.pin, 1)

    def on (self):
        self.PWM.stop ()
        GPIO.output(self.pin, GPIO.HIGH)

    def off (self):
        self.PWM.stop ()
        GPIO.output(self.pin, GPIO.LOW)        

    def flash (self):
        self.PWM.start (50)



if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    led = LED (40)
 
    while True:
        #led.on()
        #time.sleep (1)

        #led.off()
        #time.sleep (1)

        led.flash()
        #time.sleep(5)