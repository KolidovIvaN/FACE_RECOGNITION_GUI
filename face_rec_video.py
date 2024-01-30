import face_recognition
import cv2
import os
from tkinter import filedialog

database_path = './database'

known_face_encodings = []
known_face_names = []
for filename in os.listdir(database_path):
    image = face_recognition.load_image_file(os.path.join(database_path, filename))
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(os.path.splitext(filename)[0])


def select_recogniz_video():
    # Загрузка видео
    input_file = filedialog.askopenfilename()
    video_capture = cv2.VideoCapture(input_file)

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'./result/output_video.mp4', fourcc, fps, (frame_width, frame_height))

    while video_capture.isOpened():
        ret, select_video = video_capture.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(select_video, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "No match"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(select_video, (left, top), (right, bottom),
                          (0, 255, 0) if name != "No match" else (0, 0, 255),
                          thickness=4, lineType=1)
            cv2.putText(select_video, name, (left, bottom), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (255, 0, 0) if name != "No match" else (0, 0, 255), 2)

        out.write(select_video)

        cv2.imshow('Video', select_video)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
