from tkinter import *
from face_rec_photo import select_recognize_image
from face_rec_video import select_recogniz_video
from face_rec_web_cam import select_recogniz_webcam
import subprocess


def show_manual(content):
    top = Toplevel(window)
    top.title('Manual')
    text_box = Text(top)
    text_box.pack()
    text_box.insert(END, content)
    text_box.config(state='disabled')


def open_manual():
    try:
        with open('./text_file/manual', 'r') as file:
            content = file.read()
            show_manual(content)
    except FileExistsError:
        print(f'Error: No match')


def open_database():
    file_path = './text_file/Database.odt'
    try:
        subprocess.run(['libreoffice', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error{e}')


#  Основное окно приложения
window = Tk()
window.title('Распознание лиц по фото/видео')
window.geometry('600x600')
window.wm_attributes('-alpha', 1)
window.resizable(width=False, height=False)
window['bg'] = '#c8b8cc'


#  Кнопки
button_database = Button(window, text='База данных', width=12, height=2, bg='lightgrey',
                         command=open_database)
button_database.place(x=30, y=20)

button_manual = Button(window, text='Инструкция', width=12, height=2, bg='lightgrey',
                       command=open_manual)
button_manual.place(x=240, y=20)

button_exit = Button(window, text='Выход', width=12, height=2, bg='lightgrey',
                     command=window.quit)
button_exit.place(x=450, y=20)

input_label = Label(window, text='Выберите фото/видео для распознания лиц на нем:',
                    font=('DejaVuSans-Bold', 12), bg='lightgrey')
input_label.place(x=25, y=150)

button_photo = Button(window, text='Фото', width=13, height=5, bg='lightgrey',
                      font=('DejaVuSans-Bold', 20), command=select_recognize_image)
button_photo.place(x=30, y=220)

button_video = Button(window, text='Видео', width=13, height=5, bg='lightgrey',
                      font=('DejaVuSans-Bold', 20), command=select_recogniz_video)
button_video.place(x=325, y=220)

button_webcam = Button(window, text='Веб-камера', width=13, height=5, bg='lightgrey',
                       font=('DejaVuSans-Bold', 20), command=select_recogniz_webcam)
button_webcam.place(x=185, y=410)

window.mainloop()
