import RPi.GPIO as GPIO
from time import sleep

deg = 0


class stepper:
    def __init__(self,deg):
        self.board = GPIO.setmode(GPIO.BOARD)
        self.control_pins = [7,11,13,15]
        self.deg = deg
        self.seq = seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1] ]
    

    
        for pin in self.control_pins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,0)



        for i in range(150):
            for halftep in range(8):
                for pin in range(4):
                    GPIO.output(self.control_pins[pin], self.seq[halftep][pin])
                sleep(0.001)

        GPIO.cleanup()

if __name__ == '__main__':
    stepper = stepper(deg)

