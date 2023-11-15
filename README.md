# simple-attendance-system
simple attendance system using face recognition

#1. Tutorial:
   
   Step 1: download source from github
   ```sh
   $ git clone https://github.com/nguyen-tho/simple-attendance-system.git
   ```
   Step 2: install pakages by command.
   ```sh
   $ pip install -r requirements.txt
   ```
   Step 3: run program.
   run GUI.py file by command.
   ```sh
   $ python GUI.py
   ```
   or
   ```sh
   $ python3 GUI.py
   ```
   if you use python 3
   
#2. Collect data:
   - System will take a video about 350 frame, user can make several poses as much as possible to create a variety dataset

#3. Capture an image to verify:
   - When user need to check in, system will take a photo automatically for 5s after camera/webcam turned on
#4. Deepface:
   - In this project I have just used deepface to verify the identity of a person who sign up his/her information and data has been saved in our database
   - Using verify method to check an image which is similar with one random image in his/her dataset images in database
   ```sh
   from deepface import DeepFace
   verified_img =  DeepFace.verify(image, image_in_dataset, enforce_detection=False)
   #image is path of image which is captured to verify
   #image_in_dataset is path of image which is in user's dataset
   ```
   - if verified value is True -> save log
   - if not -> send alert "try again"
     
#5. Advantages and Disadvantages
   ### Advantages
   - Can recognize object in weak brigtness environment
   - When signed up user wear glasses. However, while recognition that person do not wear glass -> can recognize
   - Have a good confidence (about more than 90%)
   ### Disadvantages
   - In the first time need to download model file and weights file -> it spends too much time (about 120 seconds) depends on computer
   - Cannot detect real-time -> cannot apply to a practical project

#6. References:
   - Deep face: https://github.com/serengil/deepface .
   - UI design: https://github.com/joeVenner/FaceRecognition-GUI-APP
     
#7. New update:
   - Solve the problem "cannot detect realtime" by compare current frame from camera and verify it
   - Verify current frame with a random image in user's dataset
    
   
   
