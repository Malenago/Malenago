from tkinter import *
import tkinter as ttk
from PIL import Image, ImageTk
import os


#------------------------- разделы (кнопки) ---------------------------

# кнопки (разделение по группам)

# добавлять/удалять грузовой транспорт
# просматривать весь доступный транспорт
# просматривать грузовой транспорт по грузоподъемности

# вносить заявку на перевоз груза по указанным габаритам

# подобрать и забронировать транспорт

# просматривать занятый грузовой транспорт
# просматривать свободный грузовой транспорт

# выход

text_butt=['Просмотр и редактирование транспорта',
           'Оставить заявку на перевоз',
           'Забронировать транспорт',
           'Занятость транспорта',
           'Выйти из приложения']

#------------------------- основные настройки --------------------------

root = Tk()
root.title('logistics') #название
root.geometry('750x700') #размер окна
root.resizable(False, False) #фиксируем
font = ("LKLUG", 14) #шрифт

#------------------------ основная часть часть --------------------------

# текст - приветствие
label = ttk.Label(text="Добро пожаловать на главную страницу!",
                  pady=35,font=("LKLUG", 22),fg="#1e1d52")
label.pack()

# логотип компании
canvas= Canvas(root, width=481, height= 302)
canvas.pack()
img= ImageTk.PhotoImage(Image.open("pages/static/logo.png"))
canvas.create_image(10,10,anchor=NW,image=img)

# текст - меню
label = ttk.Label(text="Меню:",pady=20,font=("LKLUG", 22),fg="#1e1d52")
label.pack()

# функция для закрытия приложения
def close_window():
    root.destroy()

# функции для перехода между окнами
def do_saw():
    os.system('python3 pages/saw.py')

def do_appli():
    os.system('python3 pages/appli.py')

def do_book():
    os.system('python3 pages/book.py')

def do_busy():
    os.system('python3 pages/busy.py')


# генерация кнопок по названию из text_butt
for x in text_butt:
    if x=='Просмотр и редактирование транспорта':
        btn = ttk.Button(text=x, command=do_saw)
    elif x=='Оставить заявку на перевоз':
        btn = ttk.Button(text=x, command=do_appli)
    elif x=='Забронировать транспорт':
        btn = ttk.Button(text=x, command=do_book)
    elif x=='Занятость транспорта':
        btn = ttk.Button(text=x, command=do_busy)
    else:
        btn = ttk.Button(text=x, command=close_window)
    btn.pack(padx=40)

root.mainloop()