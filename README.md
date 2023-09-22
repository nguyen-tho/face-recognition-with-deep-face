# simple-attendance-system
simple attendance system using face recognition

1. Tutorial
   Step 1: install pakages by command.
   ```sh
   $ pip install -r requirements.txt
   ```
   Step 2: run program.
   run GUI.py file by command.
   ```sh
   $ python GUI.py
   ```
   or
   ```sh
   $ python3 GUI.py
   ```
   if you use python 3
2. Collect data:
   System will take a video about 350 frame, user can make several poses as much as possible to create a variety dataset

3. Capture an image to verify:
   When user need to check in, system will take a photo automatically for 5s after camera/webcam turned on
4. Deepface:
   In this project I have just used deepface to verify the identity of a person who sign up his/her information and data has been saved in our database
   Using find method to check an image which is fiited to one or more images in database
   ```sh
   from deepface import Deepface
   checklist =  DeepFace.find(image, data_path, enforce_detection=False)
   ```
   if has one or more images fitted, return verified. Otherwise, not verified
   data_path is path of folder which contain set of images when the user signed up to the system
   image is path of an image which captured to verify information of the user
5. References:
   Deep face: https://github.com/serengil/deepfacev .
   UI design: https://github.com/joeVenner/FaceRecognition-GUI-APP
   
   
