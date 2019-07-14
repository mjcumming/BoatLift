import RPi.GPIO as GPIO
import time


# Define GPIO to use on Pi
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
GPIO_TRIGGER = 16
GPIO_ECHO = 18

TRIGGER_TIME = 0.00001
MAX_TIME = 0.008  # max time waiting for response in case something is missed





class UltraSonic:

    def __init__(self):
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Echo

        GPIO.output(GPIO_TRIGGER, False)

    def measure(self): # single measurement
        # Pulse the trigger/echo line to initiate a measurement
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(TRIGGER_TIME)
        GPIO.output(GPIO_TRIGGER, False)

        # ensure start time is set in case of very quick return
        start = time.time()
        timeout = start + MAX_TIME

        # set line to input to check for start of echo response
        while GPIO.input(GPIO_ECHO) == 0 and start <= timeout:
            start = time.time()

        if(start > timeout):
            return None

        stop = time.time()
        timeout = stop + MAX_TIME
        # Wait for end of echo response
        while GPIO.input(GPIO_ECHO) == 1 and stop <= timeout:
            stop = time.time()

        if(stop <= timeout):
            elapsed = stop-start
            distance = float(elapsed * 34300)/2.0
        else:
            return None
        return distance

    def distance(self, sample_size=5, sample_wait=0.1):
        sample=[]

        for distance_reading in range(sample_size):
            distance_cm = self.measure()

            if distance_cm is not None:
                sample.append(distance_cm)

        if len (sample) > 2:
            sorted_sample = sorted(sample)
            return int(sorted_sample[sample_size // 2])
        else:
            return None


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BOARD)
        us = UltraSonic()
        while True:
            dist = us.distance()
            if dist is not None:
                print ("Measured Distance = %.1f cm" % dist)
            else:
                print ('failed to measure distance')
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()