import os
import pprint
import pygame
import json    
import pprint
import socket
import sys

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self, ip, port):
        """Listen for events to happen"""

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)          
        print ("Socket successfully created")
        
        # s.bind((ip, port))         
        # print ("socket binded to %s" %(port)) 
        # s.listen(5)      
        # print ("socket is listening")  
        
        # c, addr = s.accept()      
        # print ('Got connection from', addr) 

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        try: 
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value,3)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.button_data[event.button] = True
                    elif event.type == pygame.JOYBUTTONUP:
                        self.button_data[event.button] = False
                    elif event.type == pygame.JOYHATMOTION:
                        self.hat_data[event.hat] = event.value

                    # Insert your code on what you would like to happen for each event here!
                    # In the current setup, I have the state simply printing out to the screen.
                    
                    os.system('clear')
                    pprint.pprint(self.button_data)
                    pprint.pprint(self.axis_data, width=1)
                    print(type(self.hat_data))
                    pprint.pprint(self.hat_data)

                    data_byte = json.dumps(self.axis_data).encode('utf-8')
                    s.sendto(data_byte, (ip, port))
                    # data = s.recvfrom(4)
                    # print(data)
                    # return self.axis_data , self.hat_data, self.button_data
        except Exception as e:
            print(e)
            print('Closing Connection')
            s.close() 

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen(sys.argv[1], int(sys.argv[2]))
