 
import RPi.GPIO as GPIO
import time


class Valve:
    
    pin = None

    name = None

    def __init__(self, name, pin): # using GPIO.BOARD
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT) 

    def open (self):
        GPIO.output(self.pin, GPIO.HIGH)

    def close (self):
        GPIO.output(self.pin, GPIO.LOW)        



if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    valve = Valve (26)
 
    while True:
        valve.open()
        time.sleep (1)

        valve.close()
        time.sleep (1)
