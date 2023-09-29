import json
import os
import cv2
from flask import Flask, Response, jsonify, render_template,request, redirect, session
import numpy as np
import tensorflow as tf
from classification import classification 
import base64
import io
from PIL import Image
from flask_mysqldb import MySQL
import MySQLdb.cursors
import uuid
import re
ALLOWED_EXTENSIONS = {'jpg'}

model = tf.keras.models.load_model('D:\\SIH 2023\\Website\\keras_model.h5')

supplier = {1: '<iframe title="supplier_1" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=8c7891eb-fbda-410d-b34c-3a4c10e9661c&autoAuth=true&ctid=02286583-175c-458f-98e0-234d4b040175" frameborder="0" allowFullScreen="true"></iframe>',2:'<iframe title="supplier_2" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=ddf84a0d-631c-4362-9bfc-eec22e9c3208&autoAuth=true&ctid=02286583-175c-458f-98e0-234d4b040175" frameborder="0" allowFullScreen="true"></iframe>'}


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'devahari'
app.config['MYSQL_DB'] = 'BotonAI'

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

mysql = MySQL(app)
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
                   b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')

@app.route('/capture',methods=["POST"])
def capture():
    image = None
    image_base64 = request.form.get("image")
    
    if image_base64:
        if ',' in image_base64:
            base64_data = image_base64.split(',')[1]
            image_data = base64.b64decode(base64_data)
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is not None and image.any():
        c = classification('D:\\SIH 2023\\Website\\keras_model.h5','D:\\SIH 2023\\Website\\labels.txt')
        prediction = c.classify_image(image)
        if prediction == None:
            plant_name=request.args.get('raw_material_name')
            e_plant=re.sub(r'[^a-zA-Z]','',plant_name).lower()
            e_plant=plant_name.capitalize()
            Status="Not Verified"
            log_login_history_update(session['user_id'],e_plant,"Incorrect" ,Status)
            return jsonify({'prediction': prediction})
        
        elif prediction != None:
            plant_name=request.args.get('raw_material_name')
            e_plant=re.sub(r'[^a-zA-Z]','',plant_name).lower()
            p_plant=str(prediction.split("$")[0]).split(":")[1].strip()
            predicted=re.sub(r'[^a-zA-Z]','',p_plant).lower()
            Status=""
            p_species=str(prediction.split("$")[1]).split(":")[1].strip()
            if e_plant in predicted:
                Status="Verified"
                e_plant=plant_name.capitalize()
            else:
                e_plant=plant_name.capitalize()
                Status="Not Verified"
            log_login_history_update(session['user_id'],p_plant,p_species ,Status)
            return jsonify({'prediction': prediction})
        else:
            return jsonify({'prediction': prediction})
    else:
        return jsonify({'error': 'Invalid image data'}), 400

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        typeOfUser = request.form['role'].lower()
        unique_user_id = str(uuid.uuid4())

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO users (id, full_name, username, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)',
                       (unique_user_id, fullname, username, email,password, typeOfUser))
        mysql.connection.commit()

        log_login_history(unique_user_id, 'Registered')

        session['loggedin'] = True
        session['user_id'] = unique_user_id  
        session['username'] = username
        return redirect('/')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('login.html', msg=msg)

def log_login_history(user_id, login_status):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO user_login_history (user_id, login_status) VALUES (%s, %s)',
                   (user_id, login_status))
    mysql.connection.commit()
    cursor.close()

def log_login_history_update(user_id, predicted_plant_name,predicted_species,login_status):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO history (User_Id,Plant_Name,Plant_Species, Verified_Status) VALUES (%s, %s,%s, %s)',
                   (user_id, predicted_plant_name,predicted_species,login_status))
    mysql.connection.commit()
    cursor.close()

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id, password,role FROM users WHERE username = %s', (username,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and user_data['password'] == password:
            session['loggedin'] = True
            session['user_id'] = user_data['id']
            session['username'] = username
            session['role'] = user_data['role']
            msg = 'Logged in successfully !'
            log_login_history(user_data['id'], 'Login Successful')
            if user_data['role'] == 'chemist':
                return redirect("/chemist")  
            elif user_data['role'] == 'supplier':
                return redirect("/supplier")
        else:
            msg = 'Incorrect username or password !'
            log_login_history(user_data['id'], 'Login Failed')

    return render_template('login.html', msg=msg)
@app.route('/')
def h():
    if 'username' in session and session['role']=='supplier':
        return render_template('identification.html',username=session['username'])
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session and session['role']=='supplier':
        return render_template('index.html',username=session['username'])
    else:
        return render_template('login.html')
    


@app.route("/supplier")
def identify():
    if 'username' in session and session['role']=='supplier':
        return render_template('identification.html',username=session['username'])
    else:
        return render_template('login.html')

@app.route("/predict",methods=['GET','POST'])
def predict():
    image_input = request.files["image"]
    if image_input:
        img_bytes = image_input.read()
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        resized_image = cv2.resize(img, (224, 224))
        c = classification('D:\\SIH 2023\\Website\\keras_model.h5','D:\\SIH 2023\\Website\\labels.txt')
        prediction = c.classify_image(resized_image)
        # Predicted Name and Entered Name
        plant_name=request.args.get('raw_material_name')
        e_plant=re.sub(r'[^a-zA-Z]','',plant_name).lower()
        p_plant=str(prediction.split("$")[0]).split(":")[1].strip()
        predicted=re.sub(r'[^a-zA-Z]','',p_plant).lower()
        Status=""
        p_species=str(prediction.split("$")[1]).split(":")[1].strip()
        if e_plant in predicted:
            Status="Verified"
            e_plant=plant_name.capitalize()
        else:
            e_plant=plant_name.capitalize()
            Status="Not Verified"
        log_login_history_update(session['user_id'],p_plant,p_species ,Status)
        return prediction
    else:
        im = request.json['image']
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        resized_image = cv2.resize(img, (224, 224))
        c = classification('D:\\SIH 2023\\Website\\keras_model.h5','D:\\SIH 2023\\Website\\labels.txt')
        prediction = c.classify_image(resized_image)   
        return prediction

@app.route('/search')
def search():
    if 'username' in session and session['role']=='supplier':
        return render_template('search.html',username=session['username'])
    else:
        return render_template('login.html')

@app.route('/history')
def history():
    if 'username' in session and session['role']=='supplier':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Plant_Name,Plant_Species,date,Verified_Status from history WHERE user_id = (SELECT id FROM users WHERE username = %s)', (session['username'],))
        result = cursor.fetchall()
        return render_template('history.html',username = session['username'],result=result)
    else:
        return render_template('login.html')

@app.route('/chemist')
def technician():
    if "username" in session and session['role'] == 'chemist':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT username from users where role='supplier'")
        data=cursor.fetchall()
        print(data)
        return render_template("manufacture_identification.html",username=session['username'],data=data)
    else:
        return render_template("login.html")

@app.route('/report', methods=['GET', 'POST'])
def supplier_report():
    if request.method == 'POST':
        sup_id=request.json['sup_id']
        print(sup_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id FROM users WHERE username=(%s)",(sup_id,))
        r=cursor.fetchone()
        result = r['id']
        print(result)
        cursor.execute("SELECT iframe from user_report WHERE user_id=(%s)",(result,))
        ifm=cursor.fetchone()
        print(ifm)
    return render_template('report.html',supplier_report=ifm,username=session['username'])

@app.route('/mindex')
def mindex():
    if "username" in session and session['role'] == 'chemist':
        return render_template("manufacture_index.html",username=session['username'])
    else:
        return render_template("login.html")

@app.route('/msearch')
def msearch():
    if "username" in session and session['role'] == 'chemist':
        return render_template("manufacture_search.html",username=session['username'])
    else:
        return render_template("login.html")

@app.route('/mhistory')
def mhistory():
    if "username" in session and session['role'] == 'chemist':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Plant_Name,Plant_Species,date,Verified_Status from history WHERE user_id = (SELECT id FROM users WHERE username = %s)', (session['username'],))
        result = cursor.fetchall()
        return render_template("manufacture_history.html",username=session['username'],result=result)
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)