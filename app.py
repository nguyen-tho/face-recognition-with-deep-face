from flask import Flask, render_template, request, jsonify, Response
import cv2
from deepface import DeepFace
import os
app = Flask(__name__)
from create_dataset import get_random_jpg_file
from PIL import Image


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    # Logic for signup
    return render_template('register.html')


def user_data(name):
    # Logic to fetch user data from database
    path = "./data/" + name
    try:
        os.makedirs(path)
    except:
        return {'message': 'This user is existed'}, 400
def gen_frames(name):
    user_data(name)
        
    num_of_images=0
    cap = cv2.VideoCapture(0)  # Start capturing from webcam
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            detected_faces = DeepFace.extract_faces(frame, detector_backend='ssd', enforce_detection=False)

            if len(detected_faces) > 0:
                region = detected_faces[0]["facial_area"]
                x, y, w, h = region['x'], region['y'], region['w'], region['h']

                # Debug: print the coordinates of the detected face
                print(f"Face detected at x={x}, y={y}, width={w}, height={h}")

                if w > 0 and h > 0:  # Ensure that width and height are positive
                    cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                    cv2.putText(frame, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                else:
                    print("Invalid face coordinates!")
            img_path = f'data/{name}/'
            cv2.imwrite(img_path+name+'_'+str(num_of_images)+'.jpg', frame)
            num_of_images = num_of_images + 1
            # Encode the frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame to be used in the HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27 or num_of_images >= 100: #take 100 frames
            break
    cap.release()


@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/start_capture', methods=['GET', 'POST'])
def start_capture():
    name = request.args.get('name')  # Get name from query string (for GET requests)
    if name:
        return Response(gen_frames(name), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return {'message': 'No name provided'}, 400
    
@app.route('/verify')
def verify_page():
    return render_template('verify.html')

@app.route('/verify', methods=['POST'])
def verify_image():
    """
    Expects:
        - 'image' in form-data: an image file to verify (taken from webcam, etc.)
        - 'name' in form-data: the username whose folder exists under /data/
        
    Returns:
        JSON response with 'verified' status and 'accuracy' score
    """
    if 'image' not in request.files or 'name' not in request.form:
        return jsonify({'error': 'Missing image or username'}), 400

    image_file = request.files['image']
    username = request.form['name']
    data_path = f"data/{username}/"

    if not os.path.exists(data_path):
        return jsonify({'error': f"User data not found for '{username}'"}), 404

    target_img_path = get_random_jpg_file(data_path)
    if not target_img_path:
        return jsonify({'error': 'No image found in user folder'}), 404

    try:
        # Save uploaded image temporarily
        compare_path = "captured.jpg"
        image_file.save(compare_path)

        # Verify identity
        try:
             result = DeepFace.verify(compare_path, target_img_path, enforce_detection=False, model_name='Facenet512')
        except Exception as e:
            print("DeepFace error:", str(e))  # Log to console
            return jsonify({'error': f'DeepFace failed: {str(e)}'}), 500

        verified = bool(result['verified'])  # convert from numpy.bool_ to Python bool
        accuracy = 1 - float(result["distance"])




        # Clean up
        if os.path.exists(compare_path):
            os.remove(compare_path)

        return jsonify({'verified': verified, 'accuracy': round(accuracy, 4)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
