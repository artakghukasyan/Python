from time import sleep
import RPi.GPIO as GPIO
import threading

class stepper(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.degree = 0
        self.DIR = 27
        self.STEP = 17 

        
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR,GPIO.OUT)
        GPIO.setup(self.STEP,GPIO.OUT)
        self.GPIO_SETUP()

    def GPIO_SETUP(self):
        GPIO.output(self.DIR,1)
        GPIO.output(self.STEP,GPIO.HIGH)
        sleep(0.001)

    def TURN_RIGHT(self,degree):
        for x in range(degree):
            GPIO.output(self.DIR,1)
            GPIO.output(self.STEP,GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.STEP,GPIO.LOW)
            sleep(0.01)

    def TURN_LEFT(self,degree):
        for x in range(degree):
            GPIO.output(self.DIR,0)
            GPIO.output(self.STEP,GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.STEP,GPIO.LOW)
            sleep(0.01)
    def stop(self,degree):
        for x in range(degree):
            GPIO.output(self.STEP,GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.STEP,GPIO.LOW)
            sleep(0.01)

if __name__ == '__main__':
    s = stepper()

        
        