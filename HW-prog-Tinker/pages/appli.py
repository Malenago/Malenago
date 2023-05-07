from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox
import time
import phonenumbers

#------------------------- функции вспомогательные ---------------------------

# имитация загрузки и отправки данных
def load():

    newWindow = tk.Toplevel(root_appli)
    newWindow.geometry('300x250')  # размер окна
    newWindow.resizable(False, False)  # фиксируем
    font = ("LKLUG", 14)  # шрифт


    label1 = Label(newWindow,text='Пожалуйста, подождите',font=("LKLUG", 15),fg="#1e1d52")
    label1.place(x=60,y=50)

    for i in range(5):
        label1.config(text="Пожалуйста, подождите " + ("." * (i+1)))
        newWindow.update()
        time.sleep(0.7)

    label1.config(text="")
    newWindow.update()

    label2 = tk.Label(newWindow,text='Спасибо за заявку! \n В ближайшее время \n с Вами свяжутся',
                      font=("LKLUG", 15),fg="#1e1d52").place(x=60,y=60)

#------------------------- база данных ---------------------------

# добавление в БД
def add_db(mas):

    # подключаемся к БД, добавляем данные
    sqlite_connection = sqlite3.connect('pages/applications.db')
    cursor = sqlite_connection.cursor()

    sqlite_insert_with_param = """INSERT INTO applications
                                  (first_name,last_name, loadcapacity, length, width, height, information) 
                                  VALUES(?, ?, ?, ?, ?, ?, ?);"""

    data_tuple = (mas[0], mas[1], mas[2], mas[3], mas[4], mas[5], mas[6])
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()

#------------------------- основные настройки --------------------------

root_appli = Tk()
root_appli.title('logistics-appli') #название
root_appli.geometry('750x750') #размер окна
root_appli.resizable(False, False) #фиксируем
font = ("LKLUG", 14) #шрифт


#------------------------ основная часть часть --------------------------

# текст в шапке
label = tk.Label(text="Заявка на перевоз",
                  pady=10,font=("LKLUG", 22),fg="#1e1d52")
label.pack(pady=20)

# текст
label = tk.Label(text="Введите необходимые данные",
                  pady=5,font=("LKLUG", 15),fg="#1e1d52")
label.pack()


# добавление данных с проверкой
def add_f():
    name=name_entry.get()
    fam=fam_entry.get()
    loadc=loadc_entry.get()
    lent=len_entry.get()
    wid=wid_entry.get()
    hei=hei_entry.get()
    numb=numb_entry.get()
    inf=inf_entry.get()

    inf+=('Номер телефона:'+numb)
    s='0123456789.'
    if all(x!='' for x in [name,fam,loadc,lent,wid,hei,numb]) and \
       all(x in s for x in loadc) and \
       all(x in s for x in lent) and \
       all(x in s for x in wid) and \
       all(x in s for x in hei) and \
       all(x in s[:-1] for x in numb) and \
       phonenumbers.is_valid_number(phonenumbers.parse(numb, 'RU'))==True and \
       len(inf)<=200:
        add_db([name, fam, loadc, lent, wid, hei, inf])
        load()
    else:
        messagebox.showerror('Сообщение', 'Ошибка в вводе данных! Повторите снова')

# ввод имени
label = tk.Label(text="Введите свое имя: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
name_entry = Entry(root_appli)
name_entry.pack()


# ввод фамилии
label = tk.Label(text="Введите свою фамилию: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
fam_entry = Entry(root_appli)
fam_entry.pack()


# ввод веса груза
label = tk.Label(text="Введите массу груза (кг): ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
loadc_entry = Entry(root_appli)
loadc_entry.pack()

# ввод длины груза
label = tk.Label(text="Введите длину груза (м): ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
len_entry = Entry(root_appli)
len_entry.pack()


# ввод ширины груза
label = tk.Label(text="Введите ширину груза (м): ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
wid_entry = Entry(root_appli)
wid_entry.pack()


# ввод высоты груза
label = tk.Label(text="Введите высоту груза (м): ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
hei_entry = Entry(root_appli)
hei_entry.pack()

# ввод номера телефона
label = tk.Label(text="Введите номер телефона: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
numb_entry = Entry(root_appli)
numb_entry.pack()


# ввод дополнительной информации
label = tk.Label(text="Введите дополнительную информацию: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
inf_entry = Entry(root_appli)
inf_entry.pack()

# кнопка отправки формы
Button(root_appli, text='Отправить заявку', command=add_f).place(x=310,y=650)

# функция для закрытия окна
def close_window():
    root_appli.destroy()

btn = tk.Button(text='Закрыть окно', command=close_window).place(x=320,y=680)

root_appli.mainloop()