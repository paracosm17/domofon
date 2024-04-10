import os
import pickle

import cv2
import face_recognition

base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, "family")
os.makedirs(images_dir, exist_ok=True)

data = {}

for face_image in os.listdir(images_dir):
    name = face_image.split(".")[-2]
    image = cv2.imread(os.path.join(images_dir, face_image))
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)
    data[name] = encodings[0]


with open(os.path.join(base_dir, "faces_encodings"), "wb") as f:
    f.write(pickle.dumps(data))
