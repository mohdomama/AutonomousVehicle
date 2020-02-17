import socket 
import json
import os               
import sys


def main(ip, port):
	# Create a socket object 
	s = socket.socket()          
	  
	# connect to the server on local computer 
	s.connect((ip, port)) 
	  
	# receive data from the server 
	try:
		while True:
			# os.system('clear')
			data =s.recv(1024)
			data_dict = json.loads(data.decode('utf-8'))
			# 1 -> forward  3 -> turn
			print(data_dict)
			
		# close the connection 
	except Exception as e:
		print(e)
		print("Closing Client")
		s.close() 

if __name__ == '__main__':
	main(sys.argv[1], int(sys.argv[2]))