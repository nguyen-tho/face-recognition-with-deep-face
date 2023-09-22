import cv2
import os


def start_capture(name):
        path = "./data/" + name
        num_of_images = 0
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        try:
            os.makedirs(path)
        except:
            print('Directory Already Created')
        vid = cv2.VideoCapture(0)
        while True:

            ret, img = vid.read()
            #image = adjust_brightness(img,0.5, -30)
            new_img = None
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
            for x, y, w, h in face:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
                cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                cv2.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                new_img = img[y:y+h, x:x+w]
            cv2.imshow("Face Detection", img)
            key = cv2.waitKey(1) & 0xFF


            try :
                cv2.imwrite(str(path+"/"+name+"_"+str(num_of_images)+".jpg"), new_img)
                num_of_images += 1
            except :

                pass
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
        img = adjust_brightness(img, 0.5, 40)
        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
        if not ret:
            break  # Break the loop if no more frames are available
        for x, y, w, h in face:
            
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y+h, x:x+w]
        cv2.imshow("Face Detection", img)
        key = cv2.waitKey(1) & 0xFF
        try :
            cv2.imwrite(str(path+"/"+name+"_"+str(num_of_images)+".jpg"), new_img)
            num_of_images += 1
        except :

            pass
        if key == ord("q") or key == 27 or num_of_images > 350: #take 300 frames
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

# Step 2: Input the element to search for
    

# Step 3: Search for the element in the list
    return elements
    
