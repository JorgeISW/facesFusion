from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from PIL import Image
from stylegan2_pytorch import ModelLoader
import os

# Cargar StyleGAN2 preentrenado
model = ModelLoader(name='ffhq')  # 'ffhq' está entrenado para caras humanas

UPLOAD_FOLDER = 'static/uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def image_to_latent(image_path):
    img = Image.open(image_path).convert("RGB").resize((1024, 1024))
    latent_vector = model.latents_from_image(img)
    return latent_vector


def interpolate(latent1, latent2, alpha=0.5):
    # 'alpha' controla cuánto de cada rostro se conserva (0 = solo parent1, 1 = solo parent2)
    return latent1 * (1 - alpha) + latent2 * alpha


def latent_to_image(latent_vector, path="output.jpg"):
    img = model.image_from_latent(latent_vector)
    img.save(path)  # Guarda la imagen si deseas


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Guardar las imágenes subidas
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')

        if image1 and image2:
            image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1.filename)
            image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2.filename)

            latent_1 = image_to_latent(image1_path)
            latent_2 = image_to_latent(image2_path)

            # Mezcla con un 50% de características de cada "imagen"
            child_latent = interpolate(latent_1, latent_2, alpha=0.5)

            # Guarda el resultado
            output_filename = "output.jpg"
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            latent_to_image(child_latent, result_path)

            return render_template('index.html', uploaded_image=output_filename)

    return render_template('index.html', uploaded_image=None)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
