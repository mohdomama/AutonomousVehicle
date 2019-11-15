import RPi.GPIO as gpio
import time

class Movement:
    def __init__ (self):
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)
        gpio.setup(7 , gpio.OUT)
        gpio.setup(11 , gpio.OUT)
        gpio.setup(13 , gpio.OUT)
        gpio.setup(15 , gpio.OUT)



        self.p1 = gpio.PWM(7,50)
        self.p2 = gpio.PWM(11,50)
        self.p3 = gpio.PWM(13,50)
        self.p4 = gpio.PWM(15,50)
        
        self.p2.start(0)
        self.p1.start(0)
        
        self.p4.start(0)
        self.p3.start(0)

    def forward(self, cycle):
        self.p1.ChangeDutyCycle(cycle)
        self.p2.ChangeDutyCycle(0)

        self.p3.ChangeDutyCycle(cycle)
        self.p4.ChangeDutyCycle(0)
       
    
    def backward(self, cycle):
        self.p1.ChangeDutyCycle(0)
        self.p2.ChangeDutyCycle(cycle)

        self.p3.ChangeDutyCycle(0)
        self.p4.ChangeDutyCycle(cycle)

        
    def left(self, cycle):
        self.p1.ChangeDutyCycle(cycle)
        self.p2.ChangeDutyCycle(0)

        self.p3.ChangeDutyCycle(0)
        self.p4.ChangeDutyCycle(cycle)
        
    
    def right(self, cycle):
        self.p1.ChangeDutyCycle(0)
        self.p2.ChangeDutyCycle(cycle)

        self.p3.ChangeDutyCycle(cycle)
        self.p4.ChangeDutyCycle(0)
        


    def move(self):
        print('Here')
        self.backward(100)
        print('Blah')
        while True:
            pass
       

    def cleanup(self):
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()
        self.p4.stop()
        gpio.cleanup()



if __name__ == "__main__":
    movement = Movement()
    try:
        movement.move()
        movement.cleanup()
    except:
        movement.cleanup()



