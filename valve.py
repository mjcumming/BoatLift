 
import RPi.GPIO as GPIO
import time


class Valve:
    
    pin = None
    name = None

    def __init__(self, name, pin): # using GPIO.BOARD
        self.pin = pin
        self.name = name
        GPIO.setup(self.pin, GPIO.OUT) 

    def open(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def close(self):
        GPIO.output(self.pin, GPIO.LOW)        

    def set(self, tf):
        print ("Valve {} is {}".format (self.name,tf))
        GPIO.output(self.pin, tf)        



if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    valve = Valve ("Test", 29)
 
    while True:
        valve.set(True)
        time.sleep (1)

        valve.set(False)
        time.sleep (1)
