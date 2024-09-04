# simple-attendance-system
Apply face regcognition to check attendance of student by webcam when they are in an online class.
Up to now, I have developed 2 features:
- face recognition on one image which captured by user webcam
- face recognition on a video on user webcam.

#1. Tutorial: for face recogntion on a image
   
   Step 1: download source from github
   ```sh
   $ git clone https://github.com/nguyen-tho/face-recognition-with-deep-face.git
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
   - System will take a video about 100 frames, user can make several poses as much as possible to create a variety dataset

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
   #output is a tuple contain verified status, facial area of 2 images, cosine similarity
   #verified status: bool
   #facial area [x,y,w,h] values
   #cosine similarity is distance betwwen 2 vectors which embedded by 2 images. The less cosine the more similarity
   ```
   - if verified value is True -> save log
   - if not -> send alert "try again"
   - In new version, I use find method to find identity of user who is owner of captured photo or video
     ```sh
     from deepface import DeepFace
     verified_list = DeepFace.find(image, dataset_path, enforce_detection=False)
     #image is path of image which is captured to verify
     #dataset_path is path to dataset folder
     #output is a dataframe of similar images list
     #each row has identity, facial area amd cosine
     #identity is path of image in dataset which deepface determine they are similar with captured image
     #facial area [x,y,w,h] values
     #cosine similarity is distance betwwen 2 vectors which embedded by 2 images. The less cosine the more similarity
     ```
#5. Advantages and Disadvantages
   ### Advantages
   - Can recognize object in weak brigtness environment
   - When signed up user wear glasses. However, while recognition that person do not wear glass -> can recognize
   - Have a good confidence (about more than 90%)
   - DeepFace use pre-trained model -> do not need to train again
   ### Disadvantages
   - In the first time need to download model file and weights file -> it spends too much time (about 120 seconds) depends on computer and size if image database
   - When add a new user, system will update new pkl weight file, it consumes too much time
   - Sometimes recognition result may be wrong but confidence still high
   - When compare with DeepFace.verify method, DeepFace.find method will slower than because need time to determine identity of the captured image
   - Recognize ability maybe impacted by pre-trained model and detector backend. 

#6. References:
   - Deep face: https://github.com/serengil/deepface .
   - UI design: https://github.com/joeVenner/FaceRecognition-GUI-APP
     
#7. New update:
   - Solve the problem "cannot detect realtime" by current frame which taken by webcam and verify with user's image dataset
   - Verify current frame with a random image in user's dataset
   - Some detector backends and models can combine
     ```sh
     #some detector backend and model may suitable to use
     detector_backend = opencv, model_name = [VGG-Face, Facenet, Facenet512, ArcFace]
     detector_backend = ssd, model name = [VGG-Face, ArcFace]
     detector_backend = retinaface, model_name = VGG-Face # can use but slower than other detector backend
     #this is my personal knowledge about DeepFace. Can treat it as a reference
     ```
    
   
   
