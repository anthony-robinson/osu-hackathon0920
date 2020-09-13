import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import requests
from werkzeug.utils import secure_filename
from Fruit_Recognition.Fruit_Recognition import*

DEVELOPMENT_ENV  = True

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/error')
def error():
    return render_template('index.html', error='Fruit could not be recognized from image. Try another.')

@app.route('/results')
def results():
    files = os.listdir(app.config['UPLOAD_PATH'])
    print(files)
    return render_template('results.html', files=files)

@app.route('/results/<fruit>/<new_img>')
def get_fruit(fruit, new_img):
    response = requests.get('https://www.fruityvice.com/api/fruit/' + fruit, verify=False)
    results = response.json()
    return render_template('results.html', fruit=results, new_img=new_img)

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['image_file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return redirect(url_for('index'))

        new_image = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(new_image)
        rec = classifyFruit(new_image, load_fruits())
        if rec is not None:
            return redirect(url_for('get_fruit', fruit=rec, new_img=filename))
        else:
            return redirect(url_for('error'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)