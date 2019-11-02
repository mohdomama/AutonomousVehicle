import RPi.GPIO as gpio
import time

class Movement:
    def __init__ (self):
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)
        gpio.setup(7 , gpio.OUT)
        gpio.setup(11 , gpio.OUT)
        gpio.setup(13 , gpio.OUT)
        gpio.setup(15 , gpio.OUT)


        p1 = gpio.PWM(7,100)
        p2 = gpio.PWM(11,100)
        p3 = gpio.PWM(13,100)
        p4 = gpio.PWM(15,100)

    def move(self):
        p1.start(100)
        p2.start(100)
        p3.start(100)
        p4.start(100)

        time.sleep(2)

        p1.stop()
        p2.stop()
        p3.stop()
        p4.stop()
        gpio.cleanup()

if __name__ == "__main__":
    movement = Movement()
    movement.move()



