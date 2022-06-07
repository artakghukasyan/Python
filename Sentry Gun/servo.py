import RPi.GPIO as GPIO
from time import sleep


class servo:
    def __init__(self):
        self.tries = 0
        self.servoPin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPin,GPIO.OUT)
        GPIO.setwarnings(False)

        self.p = GPIO.PWM(self.servoPin,50)
    def fire(self):

        while self.tries == 0:
            self.p.start(2.5)
            self.p.ChangeDutyCycle(5)
            sleep(0.5)
            self.p.ChangeDutyCycle(2.5)
            sleep(0.5)
            self.tries += 1
            if self.tries > 0:
                self.p.stop()
                self.tries -= 1 
                break


if __name__ == '__main__':
    s = servo()
    s.fire()
    