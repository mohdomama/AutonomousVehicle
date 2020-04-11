import argparse
import base64
import json
import cv2

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import time
from PIL import Image
from PIL import ImageOps
from flask import Flask, render_template
from io import BytesIO

from keras.models import load_model


sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None

def preprocess_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img / 255.0
    
    img = img.reshape(-1, 160, 320, 1)

    return img

@sio.on('telemetry')
def telemetry(sid, data):
    steering_angle = data["steering_angle"]
    throttle = data["throttle"]
    speed = data["speed"]
    imgString = data["image"]
    image = Image.open(BytesIO(base64.b64decode(imgString)))
    image_array = np.asarray(image)
    img = preprocess_image(image_array)

    steering_angle = float(model.predict([img], batch_size=1))
    print(steering_angle)
    throttle = 0.1

    if float(speed) < 20:
        throttle = 1 / float(speed)

    send_control(steering_angle, throttle)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit("steer", data={
    'steering_angle': steering_angle.__str__(),
    'throttle': throttle.__str__()
    }, skip_sid=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument('model', type=str,
    help='Path to model definition json. Model weights should be on the same path.')
    args = parser.parse_args()

    model = load_model(args.model)

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)