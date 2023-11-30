
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
    #file_name = 'captured_image.jpg'
    #model = DeepFace.build_model("VGG-Face")
    start_time = time.time()
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
        confidence = detected_faces[0]["confidence"]
         
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
        cv2.imshow("Real-time Face Detection", frame)
        new_img = frame[y:y+h, x:x+w]
        elapsed_time = time.time()-start_time
        #in a moment when detected user's face capture it
        if confidence > 0.5 and elapsed_time >5: #wait 5s and capture immediately  
            break
    # Display the resulting frame
        #elapsed_time = time.time()-start_time
        #if cv2.waitKey(1) & 0xFF == ord('q') or elapsed_time > 5: #press 'q' or wait for 5s to capture an image
            
            #break
# Release the camera
    cap.release()
    cv2.destroyAllWindows()
    return new_img

def check_attendance(name):
    """_summary_

    Args:
        name (str): name of user who log in into system
        Returns:
        None
        
        description:
        this feature allow user to take a photo automatically after 5s and 
        use DeepFace.verify method to verify the taken photo and 1 random photo in database
    """

    
    image = capture_image()
    
    cv2.imshow("Result", image)
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
    check_attendance_v2()
    
 
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
        verified, _ = verified_image(frame, name)
        #new_img = frame[y:y+h, x:x+w]
        if confidence > 0.5:
           
            if verified:
                text = (name+f'  {confidence*100:.4f}%').upper()
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
    data_path = f"data/{name}/"
    target = data.get_random_jpg_file(data_path) #get random target image file in user's dataset
    
    verified_img =  DeepFace.verify(compare, target, enforce_detection=False, model_name='Facenet512')
    verified = verified_img["verified"]
    accuracy = 1 - float(verified_img["distance"])
    return verified, accuracy

def find_identity():
    """find user in database"""
    data_path = './data'
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
        
        if confidence > 0.60:
            verified_name = find_user(frame, data_path,'Facenet512')
            if verified_name[0] != "":
                text = (verified_name[0] + f'  {confidence*100:.4f}%').upper()
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            else: 
                text = "NOT FOUND IDENTITY"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                
        cv2.imshow("Real-time Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): #press 'q' to exit
            break
# Release the camera
    cap.release()
    cv2.destroyAllWindows()
        

def find_user(image, data_path, model_name='VGG-Face'):
    find_list = DeepFace.find(image, data_path, enforce_detection=False,model_name=model_name)
    find_user_df = find_list[0]

    df = pd.DataFrame(find_user_df)
    top_rows = df[df[f'{model_name}_cosine'] < 0.15]
    top_5_rows = top_rows.head(10)  # Corrected to find top 5 rows
    top_5_rows['name'] = top_5_rows['identity'].apply(data.extract_subfolder)

# Calculate the mean of 'VGG-Face_cosine' for the selected rows
    if not top_5_rows.empty:
       max_count_name = top_5_rows['name'].value_counts().idxmax()

# Filter rows with the determined name
       selected_rows = top_5_rows[top_5_rows['name'] == max_count_name]
       mean_cosine_by_name = selected_rows.groupby('name')[f'{model_name}_cosine'].mean().reset_index()
       user_name = mean_cosine_by_name['name'].iloc[0]
       acc = 1 - float(mean_cosine_by_name[f'{model_name}_cosine'].iloc[0])
       
    else:
        user_name = ""
        acc = 0
    return [str(user_name), round(acc*100, 3)]
    #return max_count_name, acc
    
#find_identity()  
#check_attendance('tho')
#check_realtime('tho')

def check_attendance_v2():
    image = capture_image()
    data_path = 'data'
    cv2.imshow("Result", image)
    verified_name = find_user(image, data_path,'Facenet512')
    if verified_name[0] != "":
       info = save_log(verified_name[0])
       messagebox.showinfo(f"Congrat {verified_name[0]} !", info[0]+ " has logged in at "+info[1] )
       
    else:
       messagebox.showinfo("Error! Cannot find identity. Please try again")
        
    cv2.destroyAllWindows() 
    
#check_attendance_v2()