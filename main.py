import socket 
import json
import os               
import sys
from Motion.Movement import Movement


def main(ip, port):
    m = Movement()
    # Create a socket object 
    s = socket.socket()          

    # connect to the server on local computer 
    s.connect((ip, port)) 

    # receive data from the server 
    try:
        while True:
            # os.system('clear')
            data =s.recv(256).strip()
            data_dict = json.loads(data.decode('utf-8'))
            # 1 -> forward  3 -> turn
            print('\nRECV:')
            f_thrust = - data_dict['1']
            r_thrust = data_dict['3']
            print(f_thrust, r_thrust)
            
            m.custom_thrust(f_thrust , r_thrust )
            s.send('ACK'.encode('utf-8'))
            
    except Exception as e:
        print(e)
        print("Closing Client")
        s.close()
        m.cleanup()
        


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))