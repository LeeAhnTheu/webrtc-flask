# import ssl
# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import base64
# import io
# from PIL import Image
# app = Flask(__name__)
# cors = CORS(app)


# # Define the index endpoint
# @app.route('/')
# def index():
#     return "Hello, world!"

# def decode_base64(base64_string):

#        decoded_string = io.BytesIO(base64.b64decode(base64_string))
#        img = Image.open(decoded_string)
#        return img.show()

# # Define the image endpoint
# @app.route('/image', methods=['POST'])
# def parse_request():
#     data = request.get_json()
#     base64_string = data.get('base64Data')
#     print(base64_string)
#     decode_base64(base64_string)
    
#     return jsonify({"message": "Data received", "data":''})



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# import os
# import ssl
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import base64
# import io
# from PIL import Image
# from datetime import datetime
# from ultralytics import YOLO

# app = Flask(__name__)
# CORS(app)

# # Load YOLO model
# model = YOLO('./best.pt')

# def decode_base64(base64_string):
#     decoded_string = io.BytesIO(base64.b64decode(base64_string))
#     img = Image.open(decoded_string)
#     return img

# def detect_fall(image):
#     results = model(image)
#     # Check if fall is detected (this will depend on your specific model and labels)
#     for result in results:
#         if result.boxes is not None:
#             for box in result.boxes:
#                 if box.cls == model.names.index('1'):  # Adjust 'fall' to your specific label for falls
#                     return True, result
#     return False, None

# def save_image_with_timestamp(image):
#     now = datetime.now()
#     date_time = now.strftime("%Y%m%d_%H%M%S")
#     directory = f'fall_frames/{now.strftime("%Y%m%d")}'
#     os.makedirs(directory, exist_ok=True)
#     image_path = f'{directory}/fall_{date_time}.jpg'
#     image.save(image_path)
#     return image_path

# # Define the index endpoint
# @app.route('/')
# def index():
#     return "Hello, world!"

# # Define the image endpoint
# @app.route('/image', methods=['POST'])
# def parse_request():
#     data = request.get_json()
#     base64_string = data.get('base64Data')
#     img = decode_base64(base64_string)
    
#     is_fall, result = detect_fall(img)
#     if is_fall:
#         image_path = save_image_with_timestamp(img)
#         return jsonify({"message": "Fall detected", "image_path": image_path})
#     else:
#         return jsonify({"message": "No fall detected"})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


import os
import ssl
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
from datetime import datetime
import torch
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

# Load YOLO model
model = YOLO('best.pt', task="detect")

def decode_base64(base64_string):
    decoded_string = io.BytesIO(base64.b64decode(base64_string))
    img = Image.open(decoded_string).convert("RGB")
    return img

def detect_fall(image):
    # Convert PIL image to OpenCV format
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    results = model(open_cv_image, device='cuda' if torch.cuda.is_available() else 'cpu', imgsz=640)
    
    for result in results:
        img = result.orig_img
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f'{model.names[int(box.cls[0].item())]} {box.conf[0]:.2f}'
            
            if int(box.cls[0].item()) == 0:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(img, 'fall', (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return True, img
    return False, open_cv_image

def save_image_with_timestamp(image):
    now = datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    directory = f'fall_frames/{now.strftime("%Y%m%d")}'
    os.makedirs(directory, exist_ok=True)
    image_path = f'{directory}/fall_{date_time}.jpg'
    cv2.imwrite(image_path, image)
    return image_path

# Define the index endpoint
@app.route('/')
def index():
    return "Hello, world!"

# Define the image endpoint
@app.route('/image', methods=['POST'])
def parse_request():
    data = request.get_json()
    base64_string = data.get('base64Data')
    print(base64_string)
    img = decode_base64(base64_string)
    
    is_fall, result_img = detect_fall(img)
    if is_fall:
        image_path = save_image_with_timestamp(result_img)
        return jsonify({"message": "Fall detected", "image_path": image_path})
    else:
        return jsonify({"message": "No fall detected"})
    
@app.route('/detect_fall_email', methods=['POST'])
def detect_fall_email():
    data = request.json
    image_path = data.get('image_path')
    user_email = data.get('user_email')

    if detect_fall_from_image(image_path):
        send_email_notification(user_email, image_path)

    return jsonify({"status": "success"})

def detect_fall_from_image(image_path):
    # Logic phát hiện té ngã từ hình ảnh
    return True  # Giả sử đã phát hiện té ngã

def send_email_notification(to_email, image_path):
    response = requests.post(
        'http://localhost:3000/send-fall-notification',  # Địa chỉ API của Node.js
        json={'toEmail': to_email, 'imagePath': image_path}
    )
    if response.status_code == 200:
        print('Email sent successfully')
    else:
        print('Failed to send email')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
