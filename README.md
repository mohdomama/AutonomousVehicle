# AutonomousVehicle
> Final year project | 
> We developed the software stack for an autonomous vehicle

The project mostly focuses on developing a Behavioral Cloning pipeline for our vehicle and its implementation on hardware. We have also worked on some state of the art lane detection and object detection techniques like LaneNet, YOLO, etc. 

### Tech Stack:
- Tensorflow
- OpenCV
- Keras
- Python


### GitHub Repository Structure:
- BehavioralCloning: directory for behavioral cloning codes. 
  - IMG: Data directory (Not Commited)
  - driving_log.csv: Details of data (Not Commited)
  - drive.py: A script to drive the `Udacity Car Simulator`
  - data_processing.py: Handy scripts for data processing
  - train.ipynb: Notebook for training the model on `Google Colaboratory`
- LaneDetection: Testing different lane detection approaches
- Motion: Utility scripts to drive Raspberry Pi based model car
- client_server: A UDP cliet-server for communication between Pi and Controller


### Here is a live demonstration of the project:-
[Live Demo](https://www.linkedin.com/posts/mohdomama_covid19-activity-6654735664971636736-BW5Y)
