from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
import os

UPLOAD_FOLDER = 'static/uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Guardar las imágenes subidas
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')

        if image1 and image2:
            image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1.filename)
            image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2.filename)
            image1.save(image1_path)
            image2.save(image2_path)
            return render_template('index.html', uploaded_image=image1.filename)

    return render_template('index.html', uploaded_image=None)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
