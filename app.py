from flask import Flask, render_template, request, redirect, url_for,send_from_directory
import os
from werkzeug.utils import secure_filename
from pipeline import deepfakes_video_predict, deepfakes_image_predict, deepfakes_audio_predict
import librosa

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4', 'flac'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('image.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            result = deepfakes_image_predict(file_path)
            return render_template('image.html', result=result, file_url=filename)
    return render_template('image.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            result = deepfakes_video_predict(file_path)
            return render_template('video.html', result=result, file_url=file_path)
    return render_template('video.html')

@app.route('/audio', methods=['GET', 'POST'])
def audio():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Load the audio file using librosa
            audio_data, sample_rate = librosa.load(file_path, sr=None)
            
            # Pass the loaded audio data and sample rate as a tuple to the prediction function
            result = deepfakes_audio_predict((audio_data, sample_rate))
            
            return render_template('audio.html', result=result, file_url=file_path)
    return render_template('audio.html')


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
