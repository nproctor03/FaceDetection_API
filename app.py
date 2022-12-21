from flask import Flask, jsonify, request
from flask_cors import CORS
from deepface import DeepFace
from deepface.detectors import FaceDetector
import cv2
import uuid

from io import BytesIO
from PIL import Image
import base64


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Success"


@app.route('/detect', methods=["POST"])
def detect():

    try:

        resp_obj = jsonify({'success': False})
        req = request.get_json()
        #detector_name = "retinaface"
        detector_name = "opencv"

        # get raw data
        if "img" in list(req.keys()):
            # Get base64 encoded string from request object
            raw_content = req["img"]
            # decode the base 64 string
            decoded_string = base64.b64decode(raw_content[22:])
            guid = uuid.uuid4()

            filepath = "temp_data\\"+str(guid)+".jpg"

            with open(filepath, "wb") as f:
                f.write(decoded_string)

            image = cv2.imread(filepath)
            # create a file object in local memory rather than disk to prevent having to to save image.
            #image_object = BytesIO(decoded_string)
            # open the image
            # image.show()

            detector = FaceDetector.build_model(detector_name)
            object = FaceDetector.detect_face(
                detector, detector_name, image, align=True)

            print(len(obj))

            if (len(obj) == 1):
                return jsonify({'success': 'True', 'FaceDetected': 'True'})
            else:
                return jsonify({'success': 'True', 'FaceDetected': 'False'})

    except Exception as e:
        print(e)
        return jsonify({'success': 'False', 'Error': "error"})


@app.route('/detect2', methods=["POST"])
def detect_2():

    try:

        resp_obj = jsonify({'success': False})
        req = request.get_json()
        #detector_name = "retinaface"
        detector_name = "opencv"

        # get raw data
        if "img" in list(req.keys()):
            # Get base64 encoded string from request object
            raw_content = req["img"]
            # decode the base 64 string
            decoded_string = base64.b64decode(raw_content[22:])
            guid = uuid.uuid4()

            filepath = "temp_data\\"+str(guid)+".jpg"

            with open(filepath, "wb") as f:
                f.write(decoded_string)

            # image = Image.open(filepath)
            # image.show()

            try:
                face = DeepFace.detectFace(img_path=filepath,
                                           target_size=(224, 224),
                                           detector_backend="opencv",
                                           enforce_detection=True
                                           )

                return jsonify({'success': 'True', 'FaceDetected': 'True'})

            except Exception as e:
                print(e)
                return jsonify({'success': 'True', 'FaceDetected': 'False'})

    except Exception as e:
        print(e)
        return jsonify({'success': 'False', 'Error': "error"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)


#    if 'image' not in request.files:
#         return jsonify({'msg': 'error: no file found'})

#     file = request.files['image']

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(img_path)

#     resp_obj = detect_face()
