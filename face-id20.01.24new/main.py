from dbfaces import *
from flask import Flask, render_template, request
import os
import base64
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random


app = Flask(__name__)
cam = cv2.VideoCapture(0)

#Первая страница
@app.route('/')
def index():
    return render_template('testgpt4.html')


@app.route('/submit_info',  methods=['GET','POST'])
def submit_info():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    cr = request.form['cr']
    insertOrUpdate(id,name,age,gender,cr)
    cam.release()
    cv2.destroyAllWindows()
    face_from_video("recorded-video.mp4",id)
    return render_template('index.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    video = request.files['video']
    video_folder = 'video'
    os.makedirs(video_folder, exist_ok=True)
    video_path = os.path.join(video_folder, 'recorded_video.webm')  # Change to .mp4 if necessary
    video.save(video_path)
    # Optionally convert to MP4 here
    return 'Video saved', 200

@app.route('/upload', methods=['POST'])
def upload():
    video = request.files['video']
    video_path = 'uploaded_video.webm'
    video.save(video_path)  # Сохранение загруженного видео на сервере

@app.route('/save_image', methods=['POST'])
def save_image():
    # Ensure there is a photo directory to save the images
    if not os.path.exists('static/photos'):
        os.makedirs('static/photos')

    # Get the image data from the POST request
    image_data = request.json['imageData']
    # The image data is a base64-encoded string with a data URL prefix
    # We need to remove the prefix and decode the image
    header, encoded = image_data.split(",", 1)
    data = base64.b64decode(encoded)

    # Save each image with a unique filename
    
    with open(f'static/photos/image_{random.randint(0,100)}.png', 'wb') as f:
        f.write(data)

    return jsonify({'message': 'Images saved successfully'})


app.run(debug=True, port = 8000)