import cv2
from deepface import DeepFace
from tkinter import messagebox
import time
import csv
import create_dataset as data
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

def check(name):
    data_path = 'data/' + name
    image = capture_image()
    code = 0
    verified_img =  DeepFace.verify(image, data_path+f'/{name}_{code}.jpg', enforce_detection=False)
    img = cv2.imread(image)
    cv2.imshow("Result", img)
    verified = verified_img["verified"]
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
    check(name)
 
check('tho')