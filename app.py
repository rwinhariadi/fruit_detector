import logging
import os

import numpy as np
from flask import Flask, jsonify, render_template, request, send_from_directory
from PIL import Image
from tensorflow.keras.models import load_model

# Inisialisasi aplikasi Flask dan folder static/templates
app = Flask(__name__, static_folder="templates/static", template_folder="templates")

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Path model
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "best_model.h5")

# Load model yang sudah dilatih
logging.info("Loading model...")
model = load_model(model_path)
logging.info("Model loaded successfully")

class_labels = {
    0: 'Apel',
    1: 'Buah Naga',
    2: 'Durian',
    3: 'Jeruk',
    4: 'Mangga',
    5: 'Manggis',
    6: 'Nenas',
    7: 'Pisang',
    8: 'Semangka'
}

# Fungsi preprocessing gambar
def preprocess_image(image, target_size=(128, 128)):
    # Konversi gambar ke format RGB jika memiliki channel tambahan seperti RGBA
    if image.mode != "RGB":
        logging.info(f"Converting image from {image.mode} to RGB")
        image = image.convert("RGB")
    
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0  # Normalisasi ke [0, 1]
    image_array = np.expand_dims(image_array, axis=0) 
    return image_array

# Endpoint utama
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint untuk file statis
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("templates/static", filename)

# Endpoint untuk menerima unggahan gambar dan memproses prediksi
@app.route("/upload", methods=["POST"])
def upload_image():
    logging.info("Received a file upload request")

    if "file" not in request.files:
        logging.error("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400

    try:
        file = request.files["file"]

        # Validasi format file gambar
        if not file.content_type.startswith("image/"):
            raise ValueError("Uploaded file is not an image")

        image = Image.open(file)
        logging.info(f"Image file opened successfully with mode: {image.mode}")

        # Preprocessing gambar
        processed_image = preprocess_image(image)
        logging.info("Image preprocessed successfully")

        # Prediksi menggunakan model
        prediction = model.predict(processed_image)
        logging.info(f"Raw model output: {prediction}")

        predicted_class_index = np.argmax(prediction)
        predicted_class_label = class_labels[predicted_class_index]
        confidence = prediction[0][predicted_class_index]

        logging.info(f"Predicted class: {predicted_class_label}, Confidence: {confidence}")

        return jsonify({
            "prediction": predicted_class_label,
            "accuracy": round(confidence * 100, 2)
        })
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return jsonify({"error": "Gagal memproses gambar"}), 500

# Menjalankan aplikasi di port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
