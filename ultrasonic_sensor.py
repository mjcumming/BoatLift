import RPi.GPIO as GPIO
import time


class UltraSonic:

    def __init__(self):
        # set GPIO Pins
        self.GPIO_TRIGGER = 37
        self.GPIO_ECHO = 40

        # set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)


    def distance(self, sample_size=5, sample_wait=0.1):
        speed_of_sound = 331.3 
        
        sample = []
        
        for distance_reading in range(sample_size):
            GPIO.output(self.GPIO_TRIGGER, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(self.GPIO_TRIGGER, False)
            echo_status_counter = 1

            while GPIO.input(self.GPIO_ECHO) == 0:
                if echo_status_counter < 1000:
                    sonar_signal_off = time.time()
                    echo_status_counter += 1
                else:
                    return None

            while GPIO.input(self.GPIO_ECHO) == 1:
                sonar_signal_on = time.time()

            time_passed = sonar_signal_on - sonar_signal_off
            distance_cm = time_passed * ((speed_of_sound * 100) / 2)
            sample.append(distance_cm)

        sorted_sample = sorted(sample)

        return int(sorted_sample[sample_size // 2])


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BOARD)
        us = UltraSonic()
        while True:
            dist = us.distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()