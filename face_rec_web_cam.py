import numpy as np
import cv2
import os
import face_recognition

known_faces = []
face_labels = []

img_file = os.listdir('./database')

for img_name in img_file:
    current_img = cv2.imread(f'./database/{img_name}')
    known_faces.append(current_img)
    face_labels.append(os.path.splitext(img_name)[0])


def get_face_encoding(imgs):
    encoding_list = []
    for img in imgs:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(img)[0]
        encoding_list.append(face_encoding)
    return encoding_list


known_face_encodings = get_face_encoding(known_faces)


def select_recogniz_webcam():
    video_capture = cv2.VideoCapture(0)
    while True:
        frame = video_capture.read()
        if frame is not None:
            frame = frame[1]
            resized_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(resized_frame)
            current_face_encodings = face_recognition.face_encodings(resized_frame, face_locations)

            for face_encoding, location in zip(current_face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    recognized_name = face_labels[best_match_index].upper()
                    top, right, bottom, left = location
                    top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

                    cv2.rectangle(frame, (left - 5, top - 5), (right + 5, bottom + 5), (0, 255, 0), 2)
                    cv2.rectangle(frame, (left - 5, bottom - 40), (right + 5, bottom + 5), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, recognized_name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (255, 0, 0), 3)
                else:
                    top, right, bottom, left = location
                    top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

                    cv2.rectangle(frame, (left - 5, top - 5), (right + 5, bottom + 5), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left - 5, bottom - 40), (right + 5, bottom + 5), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, 'No match', (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (255, 255, 255), 3)

            cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# select_recogniz_webcam()
