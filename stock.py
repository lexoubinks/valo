from flask import Flask, request
import os, logging

app = Flask(__name__)
UPLOAD_FOLDER = "/home/noa/stockage"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)

@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(filepath)
    app.logger.info(f"Fichier reçu et stocké : {f.filename}")
    return {"message": "Fichier stocké"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
