
import cv2
import os
from deepface import DeepFace

def start_capture(name):
        model = DeepFace.build_model("VGG-Face")
        path = "./data/" + name
        try:
            os.makedirs(path)
        except:
            print('Directory Already Created')
# Create a video capture object for your camera (usually 0 for built-in cameras)
        cap = cv2.VideoCapture(0)
        num_of_images = 0
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
            print(x, y, w, h)
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
            cv2.imshow("Real-time Face Detection", frame)
            new_img = frame[y:y+h, x:x+w]
            try :
                cv2.imwrite(str(path+"/"+name+"_"+str(num_of_images)+".jpg"), new_img)
                num_of_images += 1
            except :

                pass
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27 or num_of_images > 350: #take 300 frames
                break
        cv2.destroyAllWindows()
        return num_of_images
#take frames by extract a video 
def take_video(name, video):
    path = "./data/" + name
    num_of_images = 0
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    try:
        os.makedirs(path)
    except:
        print('Directory Already Created')
    vid = cv2.VideoCapture(video)
    if not vid.isOpened():
        print("Error: Could not open video file.")
        exit()
    num_of_images = 0
    while True:

        ret, img = vid.read()
        #img = adjust_brightness(img, 0.5, 40)
        new_img = None
        #grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=img, scaleFactor=1.1, minNeighbors=5)
        if not ret:
            break  # Break the loop if no more frames are available
        for x, y, w, h in face:
            
            #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
            #cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            #cv2.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y+h, x:x+w]
        cv2.imshow("Face Detection", img)
        key = cv2.waitKey(1) & 0xFF
        try :
            cv2.imwrite(str(path+"/"+name+"_"+str(num_of_images)+".jpg"), new_img)
            num_of_images += 1
        except :

            pass
        if key == ord("q") or key == 27 or num_of_images > 500: #take 500 frames
            break
        cv2.destroyAllWindows()
        return num_of_images

def adjust_brightness(frame, alpha, beta):
    # Apply brightness adjustment to a single frame
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    #alpha is constrast parameter, value of alpha is 0<alpha<1 for low constrast and >1 for high constrast
    #beta is brightness parameter, value of beta is a range of integers [-127, 127]
    return adjusted_frame

def get_nameslist():
    #get names list from data folder
    data_path = 'data'
    items = os.listdir(data_path)

# Filter the list to only include directories
    with open('nameslist.txt', 'w') as f:
        for item in items:
            if os.path.isdir(os.path.join(data_path, item)):
                f.write(item+" ")
        
def read_nameslist():
    file_path = 'nameslist.txt'
    try:
        with open(file_path, 'r') as file:
            elements = file.read().split()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    #elements = []
    return elements

def number_of_samples(name):
    data_path = 'data/'+name
    if os.path.exists(data_path):
    # List all files in the directory
        all_files = os.listdir(data_path)
    
    # Use a list comprehension to filter for .jpg files
        jpg_files = [file for file in all_files if file.endswith('.jpg')]
    
    # Count the number of .jpg files
    num_jpg_files = len(jpg_files)
    return num_jpg_files 

#print('Num of samples: '+ str(number_of_samples('tho')))
#start_capture('tho')
