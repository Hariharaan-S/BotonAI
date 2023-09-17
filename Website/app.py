import os
import cv2
from flask import Flask, render_template,request, redirect, session
import numpy as np
import tensorflow as tf
from classification import classification 
ALLOWED_EXTENSIONS = {'jpg'}

# Load the model from the .h5 file
model = tf.keras.models.load_model('D:\\SIH 2023\\Website\\keras_model.h5')

supplier = {1: '<iframe title="supplier_1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=8c7891eb-fbda-410d-b34c-3a4c10e9661c&autoAuth=true&ctid=02286583-175c-458f-98e0-234d4b040175" frameborder="0" allowFullScreen="true"></iframe>',2:'<iframe title="supplier_2" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=ddf84a0d-631c-4362-9bfc-eec22e9c3208&autoAuth=true&ctid=02286583-175c-458f-98e0-234d4b040175" frameborder="0" allowFullScreen="true"></iframe>'}


app = Flask(__name__)
output_folder = 'captured_frames'

@app.route('/capture',methods=["POST"])
def capture():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    success, frame = camera.read()

    frame_filename = os.path.join(output_folder, f"frame.jpg")
    cv2.imwrite(frame_filename, frame)

    ret, buffer = cv2.imencode('.jpg', frame)
    img_array = np.frombuffer(frame, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    resized_image = cv2.resize(img, (224, 224))
    c = classification('D:\\SIH 2023\\Website\\keras_model.h5','D:\\SIH 2023\\Website\\labels.txt')
    prediction = c.classify_image(resized_image) 
    return prediction

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def h():
    return render_template('identification.html')

@app.route('/home')
def home():
    return render_template("index.html")

@app.route("/identify")
def identify():
    return render_template("identification.html")

@app.route("/predict",methods=['GET','POST'])
def predict():

    image_input = request.files['image']
    if image_input:
        
        img_bytes = image_input.read()
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    resized_image = cv2.resize(img, (224, 224))
    c = classification('D:\\SIH 2023\\Website\\keras_model.h5','D:\\SIH 2023\\Website\\labels.txt')
    prediction = c.classify_image(resized_image)   

    # prediction = model.predict(img_batch)
    return prediction

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/technician')
def technician():
    return render_template("manufacture_identification.html")



@app.route('/r')
def r():
    return render_template("report.html",supplier_report=supplier.get(1))

@app.route('/report',methods=['GET','POST'])
def report():
    s = request.json['sup_id']
    return render_template("report.html",supplier_report=supplier.get(int(s)))

if __name__ == "__main__":
    app.run(debug=True)