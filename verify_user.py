import cv2
from deepface import DeepFace
from tkinter import messagebox
import time
import csv
import create_dataset as data
def capture_image():
    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    cap = cv2.VideoCapture(0)
    file_name = 'captured_image.jpg'

    start_time = time.time()
    while True:
    # Capture frame-by-frame
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

    # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
        cv2.imshow('Video', frame)
        elapsed_time = time.time()-start_time
        if cv2.waitKey(1) & 0xFF == ord('q') or elapsed_time > 5: #press 'q' or wait for 5s to capture an image
            cv2.imwrite(file_name, frame)
            break

# Release the camera
    cap.release()
    cv2.destroyAllWindows()
    return file_name

def check(name):
    data_path = 'data/' + name
    image = capture_image()
    checklist =  DeepFace.find(image, data_path, enforce_detection=False)
    img = cv2.imread(image)
    cv2.imshow("Result", img)
    #set threshold >0.5 to check the result
    threshold = len(checklist)/data.number_of_samples(name)*1.0
    
    if threshold > 0.5:
        info = save_log(name)
        messagebox.showinfo("Congrat", info[0]+ " has checked in at "+info[1] )
       
    else:
       messagebox.showerror("Error", "Is not "+ name+" . Please try again")
       
def save_log(name):
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    
    # Create a list with student name and time
    log_data = [name, time_string]
    
    with open('logs.csv', 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the data to the CSV file
        csv_writer.writerow(log_data)
    
    return log_data
              
def main_app(name):
    check(name)
 
#check('tho1')