 
import RPi.GPIO as GPIO
import time

BLOWER_PIN = 37

class Blower_Motor:
    
    pin = None

    def __init__(self): # using GPIO.BOARD
        self.pin = BLOWER_PIN
        GPIO.setup(self.pin, GPIO.OUT) 

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)        
  



if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    motor = Blower_Motor ()
 
    while True:
        motor.on()
        time.sleep (1)

        motor.off()
        time.sleep (1)
