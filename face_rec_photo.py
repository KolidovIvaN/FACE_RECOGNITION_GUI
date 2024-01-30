import face_recognition
import cv2
import os
import numpy as np
from tkinter import filedialog

known_faces = []
face_labels = []
image_files = os.listdir('./database')

for img_name in image_files:
    current_img = cv2.imread(f'database/{img_name}')
    known_faces.append(current_img)
    face_labels.append(os.path.splitext(img_name)[0])


def get_face_encodings(images):
    encoding_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(img)[0]
        encoding_list.append(face_encoding)
    return encoding_list


known_face_encodings = get_face_encodings(known_faces)


def select_recognize_image():
    input_file = filedialog.askopenfilename()
    if input_file:
        select_img = cv2.imread(input_file)
        select_img_RGB = cv2.cvtColor(select_img, cv2.COLOR_BGR2RGB)
        selected_face_encodings = face_recognition.face_encodings(select_img_RGB)
        match_found = False
        if not selected_face_encodings:
            print('No faces found in the selected image')
        else:
            for face_encoding in selected_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    recognized_name = face_labels[best_match_index].upper()
                    top, right, bottom, left = face_recognition.face_locations(select_img_RGB)[0]
                    cv2.rectangle(select_img, (left - 5, top - 5), (right + 5, bottom + 5), (0, 255, 0), thickness=5,
                                  lineType=2)
                    cv2.putText(select_img, recognized_name, (left, bottom - 10), cv2.FONT_HERSHEY_COMPLEX,
                                3, (255, 0, 0), 3)
                    match_found = True
                    break

            if not match_found:
                top, right, bottom, left = face_recognition.face_locations(select_img_RGB)[0]
                cv2.rectangle(select_img, (left - 5, top - 5), (right + 5, bottom + 5), (0, 0, 255), thickness=6,
                              lineType=2)
                cv2.putText(select_img, "No match", (left, bottom - 10), cv2.FONT_HERSHEY_COMPLEX, 3,
                            (0, 0, 255), 3)

            if cv2.waitKey(1) & 0xFF == 27:
                exit()

            cv2.namedWindow('Распознанное(ые) лицо(а)', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Распознанное(ые) лицо(а)', width=600, height=600)
            cv2.imshow('Распознанное(ые) лицо(а)', select_img)
            cv2.imwrite(f'./result/{recognized_name}.jpg', select_img) if matches[best_match_index] else cv2.imwrite(
                f'./result/result.jpg', select_img)
            known_faces.clear()

            cv2.waitKey(0)
            cv2.destroyAllWindows()
