from flask import Flask, render_template, request, jsonify
import cv2
from deepface import DeepFace

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    # Logic for signup
    return render_template('register.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    name = request.form.get('name')
    create_dataset(name)
    return jsonify({"message": f"Dataset creation started for {name}"})
import os
def create_dataset(name):
    model = DeepFace.build_model("VGG-Face")
    path = "./data/" + name
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('Directory Already Created')

    cap = cv2.VideoCapture(0)
    num_of_images = 0

    while True:
        ret, frame = cap.read()
        detected_faces = DeepFace.extract_faces(frame, detector_backend='ssd', enforce_detection=False)

        if len(detected_faces) > 0:
            region = detected_faces[0]["facial_area"]
            x, y, w, h = region['x'], region['y'], region['w'], region['h']

            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
            new_img = frame[y:y+h, x:x+w]
            cv2.putText(frame, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(frame, str(num_of_images)+" images captured", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))

            try:
                cv2.imwrite(str(path+"/"+name+"_"+str(num_of_images)+".jpg"), new_img)
                num_of_images += 1
            except:
                pass

        cv2.imshow("Real-time Face Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27 or num_of_images >= 100:  # Capture 100 frames
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    app.run(debug=True)
