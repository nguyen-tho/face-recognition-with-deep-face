
import cv2
from deepface import DeepFace
from tkinter import messagebox
import time
import csv
import create_dataset as data
import os
import re
import pandas as pd 

def capture_image():
    start_time = time.time()
    file_name = 'captured_image.jpg'
    model = DeepFace.build_model("VGG-Face")
# Create a video capture object for your camera (usually 0 for built-in cameras)
    cap = cv2.VideoCapture(0)
        
    while True:
    # Capture a frame from the camera
        ret, frame = cap.read()

     #Perform face detection on the frame
        detected_faces = DeepFace.extract_faces(frame, detector_backend='ssd',
                                        enforce_detection=False)

        region = detected_faces[0]["facial_area"]
    #print(region)
        x = region['x']
        y = region['y']
        w = region['w']
        h = region['h']
            
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
        new_img = frame[y:y+h, x:x+w]
        cv2.imshow("Real-time Face Detection", frame)
        
    # Display the resulting frame
        elapsed_time = time.time()-start_time
        if cv2.waitKey(1) & 0xFF == ord('q') or elapsed_time > 5: #press 'q' or wait for 5s to capture an image
            cv2.imwrite(file_name, new_img)
            break
# Release the camera
    cap.release()
    cv2.destroyAllWindows()
    return file_name

def check_attendance(name):
    """_summary_

    Args:
        name (_type_): _description_
    """
    
    image = capture_image()
    
    img = cv2.imread(image)
    cv2.imshow("Result", img)
    verified =verified_image(image, name)
    #set threshold >0.5 to check the result
    #threshold = len(checklist)/data.number_of_samples(name)

    if verified:
        info = save_log(name)
        messagebox.showinfo("Congrat", info[0]+ " has checked in at "+info[1] )
       
    else:
        messagebox.showinfo("Error", "You are not "+ name+" . Please try again")
        
    cv2.destroyAllWindows()
       
def save_log(name):
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
    
    # Create a list with student name and time
    log_data = [name, time_string]
    
    with open('logs.csv', 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the data to the CSV file
        csv_writer.writerow(log_data)
    
    return log_data
              
def main_app(name):
    check_attendance(name)
 
def check_realtime(name):
    data_path = 'data/' + name
    cap = cv2.VideoCapture(0)
    while True:
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
        #new_img = frame[y:y+h, x:x+w]
        if confidence > 0.5:
            verified = verified_image(frame, name)
            if verified:
                text = (name+f'  {confidence:.4f}').upper()
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            else: 
                text = "UNVERIFIED"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Real-time Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): #press 'q' to exit
            break
# Release the camera
    cap.release()
    cv2.destroyAllWindows()

def verified_image(compare, name):
    """_summary_

    Args:
        compare (Any): an image take by webcam, camera
        name (str): username who was signed up to the system and had image data folder
        
        Returns: status of method DeepFace.verify (boolean)
    """
    # code (integer): the number of file name such as tho_30.jpg, code is 30
    code = data.random_code(data.number_of_samples(name)) #generate random code based on number of image in user data
    data_path = f"data/{name}/"
    verified_img =  DeepFace.verify(compare, data_path+f'{name}_{code}.jpg', enforce_detection=False)
    verified = verified_img["verified"]
    return verified

def check_identity():
    """find user in database"""
    data_path = 'image_data'
    cap = cv2.VideoCapture(0)
    while True:
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
        if confidence > 0.5:
            verified_name = find_user(frame, 'image_data')
            if verified_name != "":
                text = (verified_name+f'  {confidence:.4f}').upper()
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            else: 
                text = "UNVERIFIED"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Real-time Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): #press 'q' to exit
            break
# Release the camera
    cap.release()
    cv2.destroyAllWindows()
        
def find_user(image, data_path):
    name = ''
    data = DeepFace.find(image, data_path , enforce_detection=False, model_name='Facenet512')
    input_string = str(data[0]["identity"])
    match = re.search(r'image_data/(\w+).jpg', input_string)

    if match:
        name = match.group(1)
    
    # Create the formula string based on the extracted 'name'
    return name
    
check_identity()    
