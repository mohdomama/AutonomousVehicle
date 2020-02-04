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

    def left(self, cycle): #left
        self.p1.ChangeDutyCycle(cycle)
        self.p2.ChangeDutyCycle(0)

        self.p3.ChangeDutyCycle(cycle)
        self.p4.ChangeDutyCycle(0)
       
    
    def right(self, cycle):  #right
        self.p1.ChangeDutyCycle(0)
        self.p2.ChangeDutyCycle(cycle)

        self.p3.ChangeDutyCycle(0)
        self.p4.ChangeDutyCycle(cycle)

        
    def backward(self, cycle): #backward
        self.p1.ChangeDutyCycle(cycle)
        self.p2.ChangeDutyCycle(0)

        self.p3.ChangeDutyCycle(0)
        self.p4.ChangeDutyCycle(cycle)
        
    
    def forward(self, cycle): #forward
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
        max_thrust = 30
        try:
            while True:
                image = cam.read()
                cam.mask_image(lower[i], upper[i])
                centroid = cam.centroid_if_object_present()
                if centroid:
                    cx, cy = centroid
                    center = float(image.shape[1] / 2)
                    
                    diff_per = (cx - center) / (center)
                    
                    print('Diff_Per ', diff_per)
                    if diff_per > 0.2:
                        print('Going Right')
                        thrust = abs(diff_per) * max_thrust 
                        self.right(thrust)
                    elif diff_per < -0.2:
                        print('Going Left')
                        thrust = abs(diff_per) * max_thrust 
                        self.left(thrust)
                    else:
                        self.forward(40)
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
#         movement.forward(80)
#         time.sleep(2)
#         movement.backward(80)
#         time.sleep(2)
#         movement.left(80)
#         time.sleep(2)
#         movement.right(80)
#         time.sleep(2)
        movement.move()
    except Exception as e:
        print(e)
        movement.cleanup()



