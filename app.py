
from flask import Flask, render_template, request, jsonify, Response
import cv2
from deepface import DeepFace
import os
app = Flask(__name__)
from create_dataset import get_random_jpg_file
from verify_user import verified_image
from verify_user import update_pkl_file
from verify_user import find_user

import base64

webcam_active = True

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
def capture_data(name):
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
    
    #update the pkl file for new user
    update_pkl_file(name)


@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/start_capture', methods=['GET', 'POST'])
def start_capture():
    name = request.args.get('name')  # Get name from query string (for GET requests)
    if name:
        return Response(capture_data(name), mimetype='multipart/x-mixed-replace; boundary=frame')
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
             verified, accuracy = verified_image(compare_path, username)
        except Exception as e:
            print("DeepFace error:", str(e))  # Log to console
            return jsonify({'error': f'DeepFace failed: {str(e)}'}), 500

        verified = bool(verified)  # convert from numpy.bool_ to Python bool
        accuracy = float(accuracy)  # convert from numpy.float64 to Python float

        # Clean up
        if os.path.exists(compare_path):
            os.remove(compare_path)

        return jsonify({'verified': verified, 'accuracy': round(accuracy, 4)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_frames_verify(username):
    cap = cv2.VideoCapture(0)  # Start capturing from webcam
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            try:
                faces = DeepFace.extract_faces(frame, detector_backend='ssd', enforce_detection=False)
                if faces:
                    region = faces[0]["facial_area"]
                    x = region['x']
                    y = region['y']
                    w = region['w']
                    h = region['h']
                    confidence = faces[0]["confidence"]

                    verified, _ = verified_image(frame, username)

                    if confidence > 0.5:
                        if verified:
                            text = ('VERIFIED: '+username+f'  {confidence*100:.2f}%').upper()
                            color = (0, 255, 0)
                        else:
                            text = "UNVERIFIED"
                            color = (0, 0, 255)

                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(frame, text, (x, y - 4), cv2.FONT_HERSHEY_PLAIN, 1, color, 1, cv2.LINE_AA)
            except Exception as e:
                print("Error:", e)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    
@app.route('/verify_realtime')
def verify_realtime_page():
    return render_template('verify_realtime.html')

@app.route('/verify_realtime_stream')
def verify_realtime():
    username = request.args.get('username')
    return Response(generate_frames_verify(username), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/find_user')
def find_user_page():
    return render_template('find.html')


def find_identity():
    """find user in database"""
    data_path = './data'
    cap = cv2.VideoCapture(0)
    global webcam_active
    while webcam_active:
        # Capture frame-by-frame
        ret, frame = cap.read()
        faces = DeepFace.extract_faces(frame, detector_backend='ssd',
                                        enforce_detection=False)
        region = faces[0]["facial_area"]
    #print(region)
        x = region['x']
        y = region['y']
        w = region['w']
        h = region['h']
        
        confidence = faces[0]["confidence"]
        
        if confidence > 0.60:
            verified_name = find_user(frame, data_path,'Facenet512')
            if verified_name[0] != "":
                text = ('FOUND: '+verified_name[0] + f'  {confidence*100:.4f}%').upper()
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            else: 
                text = "NOT FOUND IDENTITY"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                
        #cv2.imshow("Real-time Face Detection", frame)
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield the frame to be used in the HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # Clean up
# Release the camera
    cap.release()
    
@app.route('/find_user_stream')
def find_user_stream():
    global webcam_active
    webcam_active = activate_webcam()
    # Check if the webcam is active
    return Response(find_identity(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/quit_webcam', methods=['POST'])
def quit_webcam():
    global webcam_active
    webcam_active = False
    print("Received request to stop webcam.")
    return '', 200


def activate_webcam():
    global webcam_active
    webcam_active = True
    print("Webcam activated.")
    return activate_webcam

@app.route('/find_users_realtime')
def find_user_realtime_page():
    return render_template('find_realtime.html')

def find_users_realtime():
    data_path = './data'
    cap = cv2.VideoCapture(0)
    global webcam_active
    while webcam_active:
        ret, frame = cap.read()
        faces = DeepFace.extract_faces(frame, detector_backend='ssd', enforce_detection=False)
        verified_users = []  # A list to store verified users and their confidence scores
        
        for face in faces:
            region = face["facial_area"]
            x = region['x']
            y = region['y']
            w = region['w']
            h = region['h']
            confidence = face["confidence"]
            
            if confidence > 0.6:
                verified_name = find_user(frame, data_path)
                if verified_name:
                    verified_users.append((verified_name, confidence))
                else:
                    verified_users.append(("UNVERIFIED", confidence))
                
                # Draw bounding boxes and text for each detected face
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0) if verified_name else (0,0,255), 2) 
                text = (verified_name).upper() if verified_name else "UNVERIFIED"
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0) if verified_name else (0, 0, 255), 1, cv2.LINE_AA)
        
        # Display the frame with bounding boxes and text
        #cv2.imshow("Real-time Face Detection", frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        # Yield the frame to be used in the HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # Release the camera
    cap.release()
   


@app.route('/find_users_realtime_stream')
def find_user_realtime_stream():
    global webcam_active
    webcam_active = activate_webcam()
    # Check if the webcam is active
    return Response(find_users_realtime(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)
