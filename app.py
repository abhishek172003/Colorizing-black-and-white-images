from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import cv2
import os
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)

# Model paths
DIR = os.path.dirname(os.path.abspath(__file__))
PROTOTXT = os.path.join(DIR, "model/colorization_deploy_v2.prototxt")
POINTS = os.path.join(DIR, "model/pts_in_hull.npy")
MODEL = os.path.join(DIR, "model/colorization_release_v2.caffemodel")

# Load the Model
print("Loading model...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS)

# Load centers for ab channel quantization used for rebalancing
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def process_image(image_data):
    # Decode base64 image
    nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process image
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    
    # Convert processed image to base64
    _, buffer = cv2.imencode('.png', colorized)
    colorized_b64 = base64.b64encode(buffer).decode('utf-8')
    return f'data:image/png;base64,{colorized_b64}'

@app.route('/colorize', methods=['POST'])
def colorize():
    try:
        data = request.json
        image_data = data['image']
        colorized_image = process_image(image_data)
        return jsonify({'colorized': colorized_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_static():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)