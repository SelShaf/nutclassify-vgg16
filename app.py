# app.py
# Flask app untuk klasifikasi jenis kacang-kacangan dengan model VGG16

from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

model = tf.keras.models.load_model("model_vgg16_nuts.keras")

# urutan kelas ini mengikuti class_indices dari flow_from_directory saat training
class_names = [
    'almonds',
    'brazil nuts',
    'cashews',
    'coconut',
    'hazelnuts',
    'macadamia',
    'pecans',
    'pine nuts',
    'pistachios',
    'walnuts'
]

def preprocess_image(image):
    image = image.convert("RGB").resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route("/")
def home():
    return render_template("index.html", classes=class_names)

@app.route("/klasifikasi")
def klasifikasi():
    return render_template("klasifikasi.html")

@app.route("/tentang-dataset")
def tentang_dataset():
    return render_template("tentang_dataset.html", classes=class_names)

@app.route("/cara-penggunaan")
def cara_penggunaan():
    return render_template("cara_penggunaan.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Tidak ada file yang dipilih"}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        processed = preprocess_image(image)

        prediction = model.predict(processed)[0]
        sorted_idx = np.argsort(prediction)[::-1]

        top_result = {
            "label": class_names[sorted_idx[0]],
            "confidence": round(float(prediction[sorted_idx[0]]) * 100, 2)
        }

        # 2-3 kemungkinan lain di luar prediksi utama
        other_results = [
            {
                "label": class_names[i],
                "confidence": round(float(prediction[i]) * 100, 2)
            }
            for i in sorted_idx[1:3]
        ]

        return jsonify({
            "prediction": top_result,
            "others": other_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)