import os
import pickle
import time

import cv2
import face_recognition

from logger import logger
from ufanet import Ufanet


def compare(family_faces, face):
    for human in family_faces:
        comparison = face_recognition.compare_faces([family_faces[human]], face, tolerance=0.6)
        if (len(comparison) > 0) and (comparison[0]):
            logger.info(f"Определён {human}")
            return True
    return False


def main(caption: cv2.VideoCapture, family_faces, domofon, process_this_frame=True):
    last_open = 0
    while 1:
        if caption.isOpened():
            ret, frame = caption.read()
            if not ret:
                continue
            if time.time() - last_open >= 15:
                if process_this_frame:
                    try:
                        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                        face_locations = face_recognition.face_locations(rgb_frame)
                    except:
                        process_this_frame = not process_this_frame
                        continue
                    if face_locations:
                        try:
                            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                        except IndexError:
                            process_this_frame = not process_this_frame
                            continue

                        if compare(family_faces, face_encodings):
                            domofon.open_door()
                            logger.info("Дверь открыта")
                            last_open = time.time()
                            process_this_frame = not process_this_frame
                            continue
                        else:
                            process_this_frame = not process_this_frame
                            continue
                process_this_frame = not process_this_frame
        else:
            return


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    faces_dir = os.path.join(base_dir, "family")
    assert os.path.exists(os.path.join(base_dir, "faces_encodings")), "Face encodings does not exists. " \
                                                                      "Run create_encodings.py"
    with open(os.path.join(base_dir, "faces_encodings"), "rb") as file:
        encodings = pickle.loads(file.read())

    while 1:
        login = os.getenv("UFANET_LOGIN")
        password = os.getenv("UFANET_PASSWORD")
        ufa = Ufanet(login, password)
        cap = cv2.VideoCapture(ufa.get_stream_url())
        main(cap, encodings, ufa)
