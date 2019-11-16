import RPi.GPIO as gpio
import time
import camera
import numpy as np

class Movement:
    def __init__ (self):
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(True)
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

    def backward(self, cycle):
        self.p1.ChangeDutyCycle(cycle)
        self.p2.ChangeDutyCycle(0)

        self.p3.ChangeDutyCycle(cycle)
        self.p4.ChangeDutyCycle(0)
       
    
    def forward(self, cycle):
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
        
    def stop(self):
        self.p1.ChangeDutyCycle(0)
        self.p2.ChangeDutyCycle(0)

        self.p3.ChangeDutyCycle(0)
        self.p4.ChangeDutyCycle(0)
        


    def move(self):
        i=0
        lower = [
        np.array([115, 0, 0]),  # Red
        np.array([87, 0, 0]),   # Yellow
        np.array([50, 0, 0])]   # Green
        upper = [
        np.array([135, 255, 255]),
        np.array([92, 255, 255]),
        np.array([77, 255, 255])]
        print('Love')
        cam = camera.Camera()
        
        try:
            while True:
                image = cam.read()
                cam.mask_image(lower[i], upper[i])
                centroid = cam.centroid_if_object_present()
                if centroid:
                    cx, cy = centroid
                    center = float(image.shape[1] / 2)
                    
                    diff_per = (cx - center) / (2 * center)
                    
                    print('Diff_Per ', diff_per)
                    if diff_per > 0.2:
                        print('Going Right')
                        self.right(100)
                    elif diff_per < -0.2:
                        print('Going Left')
                        self.left(100)
                    else:
                        self.forward(100)
                else:
                    self.stop()
                    
                    
        except Exception as e:
            print(e)
            cam.tearDown()
         
       

    def cleanup(self):
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()
        self.p4.stop()
        gpio.cleanup()



if __name__ == "__main__":
    movement = Movement()
    try:
        movement.forward(50)
        time.sleep(2)
        
    except Exception as e:
        print(e)
        movement.cleanup()



