import base64
import os
from flask import Flask, jsonify, render_template, request,Response, session
import cv2
from IPython.display import IFrame
import numpy as np
import pandas as pd
import mysql.connector
from classification import classification
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# MySQL configuration
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="devahari",
#     database="trashtriage"
# )

def preprocess_frame(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

output_folder = 'captured_frames'

def generate_frames():
    camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame_filename = os.path.join(output_folder, f"frame.jpg")
            cv2.imwrite(frame_filename, frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# cursor = db.cursor()
@app.route('/classify')
def classify():
    classf = classification('keras_model.h5','labels.txt')
    prediction = classf.classify_image("captured_frames\\frame.jpg")
            
    return jsonify(prediction)
    
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/segregate')
def segregate():
    return render_template('segregate.html')
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')





@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/services')
def services():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
