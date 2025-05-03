# Face recognition on raspberry pi to train KNN classifier and predications trained model and openCV encodings

import face_recognition
import picamera
import numpy as np
import cv2
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG'}


camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image")
student_image = face_recognition.load_image_file("student.jpg")
student_face_encoding = face_recognition.face_encodings(student_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
i=0

def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):


    # load all training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # load all images of student
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

          

                # Add face encoding for current image to the training set
            X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
            y.append(class_dir)

    # find  neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save  trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf

def predict(X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
   
    if knn_clf is None and model_path is None:
        raise Exception("check if model is availble or not")

    # Load trained KNN model
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)  # this is instance of knn classifier

    X_face_locations = face_recognition.face_locations(X_frame) #frame on which prediction will be made

    # If no faces are found in the image send empty arr
    if len(X_face_locations) == 0:
        return []

    # Find face encodings
    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

    # Use  KNN model to find the best matches from availble test folder faces
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    myface_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))] ## distance threshold

    # make prediction on  classes and remove  that aren't within the distance threshold value, high threshold means more mis classified
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, myface_matches)]

print("Training KNN classifier...")
classifier = train("knn_examples/train", model_path="trained_knn_model.clf", n_neighbors=5)
print("Training complete!")
    # process one frame in every 30 frames
process_this_frame = 29

while i<100:
    
    print("Capturing image.")
    # Take single frame
    camera.capture(output, format="rgb")

    # find face and face encodings 
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    i=i+1

    try:
        if process_this_frame % 30 == 0:
            predictions = predict(output, model_path="trained_knn_model.clf")
            frame = show_prediction_labels_on_image(frame, predictions)
    except:
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([student_encoding], face_encoding)
            name = "<Unknown Person>"

            if match[0]:
                name = "Student"

            print("I see someone named {}!".format(name))
        
## Segments of code taken from https://github.com/ageitgey/face_recognition
