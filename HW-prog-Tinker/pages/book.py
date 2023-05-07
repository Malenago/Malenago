from tkinter import *
import tkinter as tk
import sqlite3
import os
import phonenumbers
import time
from tkinter import messagebox
import datetime
import random

#------------------------- функции вспомогательные ---------------------------

# имитация загрузки и отправки данных
def load():
    newWindow = tk.Toplevel(root_book)
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

    label2 = tk.Label(newWindow,text='Спасибо за бронь! \n Данные отправлены \n успешно',
                      font=("LKLUG", 15),fg="#1e1d52").place(x=60,y=60)


# проверка корректности времени
def check_date(st):
    st=st.replace(',',' ')
    st=st.split(' ')
    while '' in st:
        st.remove('')

    day1, time1, day2, time2 = st[0],st[1],st[2],st[3]

    answ=day1, time1, day2, time2
    try:
        day1 = day1.split('.')
        day2 = day2.split('.')
        time1 = time1.split(':')
        time2 = time2.split(':')
        c1=datetime.datetime(int(day1[2]), int(day1[1]), int(day1[0]),int(time1[0]),int(time1[1]))
        c2=datetime.datetime(int(day2[2]), int(day2[1]), int(day2[0]), int(time2[0]), int(time2[1]))
        if c1<=c2:
            return 1,answ[0],answ[1],answ[2],answ[3]
        else:
            return 0, 0, 0, 0, 0
    except:
        return 0,0,0,0,0

# перевод даты в нужный формат
def dates(dt):
        return [int(dt[6:]), int(dt[3:5]), int(dt[0:2])]

# ------------------------- база данных ---------------------------

# добавление в БД
def add_db(mas):

    # подключаемся к БД, добавляем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_insert_with_param = """INSERT INTO history
                                  (id, id_tr, order_description, start_date, end_date, start_time, end_time, inf) 
                                  VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""

    data_tuple = (random.randint(10,20000),mas[0], mas[1], mas[2], mas[4], mas[3], mas[5], mas[6])
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()

# проверка пересечений заказов
def check_ord(id,day1,time1,day2,time2):

    # для сохранения загруженности транспорта
    count_all=0
    count=0

    # подключаемся к БД, берем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """SELECT * from history WHERE id_tr = ? """
    cursor.execute(sqlite_select_query, (id,))
    records = cursor.fetchall()

    day1 = day1.split('.')
    day2 = day2.split('.')
    time1 = time1.split(':')
    time2 = time2.split(':')

    # определяем загруженность для конкретного выбранного дня
    for row in records:
        count_all+=1
        f_1 = dates(row[3])
        f_2 = dates(row[4])
        t_1 = row[5].split(':')
        t_2 = row[6].split(':')


        a1=datetime.datetime(int(day1[2]), int(day1[1]), int(day1[0]),int(time1[0]),int(time1[1]))
        a2=datetime.datetime(int(day2[2]), int(day2[1]), int(day2[0]), int(time2[0]), int(time2[1]))

        b1=datetime.datetime(int(f_1[0]), int(f_1[1]), int(f_1[2]),int(t_1[0]),int(t_1[1]))
        b2=datetime.datetime(int(f_2[0]), int(f_2[1]), int(f_2[2]),int(t_2[0]),int(t_2[1]))

        if (a1<b1 and a2<=b1) or (b2<=a1 and b2<a2):
            count+=1

    cursor.close()
    sqlite_connection.close()

    return count_all==count

#------------------------- основные настройки --------------------------

root_book = Tk()
root_book.title('logistics-book') #название
root_book.geometry('600x610') #размер окна
root_book.resizable(False, False) #фиксируем
font = ("LKLUG", 14) #шрифт

#------------------------ основная часть часть --------------------------

# текст в шапке
label = tk.Label(text="Бронирование транспорта",
                  pady=20,font=("LKLUG", 22),fg="#1e1d52")
label.pack()


# текст
label = tk.Label(text="Подберите свободный транспорт",
                  pady=5,font=("LKLUG", 15),fg="#1e1d52")
label.pack()


# функция для открытия другой вкладки
def get_free():
    os.system('python3 pages/busy.py')

# кнопка для обновления данных
Button(root_book, text="Подобрать",
       command=get_free).pack(pady=5)


# для проверки и отправки данных
def get():
    name=name_entry.get()
    numtr=numtr_entry.get()
    dat=dat_entry.get()
    numb=numb_entry.get()
    inf=inf_entry.get()

    inf_cl=f'Номер телефона: {numb}, ИФ: {name}'
    check=check_date(dat)
    if check[0]==1 and phonenumbers.is_valid_number(phonenumbers.parse(numb, 'RU'))==True and \
       len(inf)<=200 and check_ord(int(numtr),check[1], check[2], check[3], check[4])==1:
                add_db([int(numtr), inf, check[1], check[2], check[3], check[4], inf_cl])
                load()
    else:
        messagebox.showerror('Сообщение', 'Ошибка в вводе данных! Повторите снова')

# текст
label = tk.Label(text="Заполните необходимые данные",
                  pady=5,font=("LKLUG", 15),fg="#1e1d52")
label.pack()

# ввод имени
label = tk.Label(text="Введите свои ФИО: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
name_entry = Entry(root_book)
name_entry.pack()


# ввод номера транспорта
label = tk.Label(text="Введите ВН транспорта, \n который хотите забронировать: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
numtr_entry = Entry(root_book)
numtr_entry.pack()

# ввод даты
label = tk.Label(text="Введите дату доставки в формате \n 'ДД.ММ.ГГ ЧЧ:ММ, ДД.ММ.ГГ ЧЧ:ММ': ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
dat_entry = Entry(root_book)
dat_entry.pack()


# ввод номера телефона
label = tk.Label(text="Введите номер телефона: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
numb_entry = Entry(root_book)
numb_entry.pack()

# ввод дополнительной информации
label = tk.Label(text="Введите дополнительную информацию: ",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack(pady=5)

# поле ввода
inf_entry = Entry(root_book)
inf_entry.pack()


# кнопка
Button(root_book, text="Забронировать",
       command=get).pack(pady=5)


# функция для закрытия окна
def close_window():
    root_book.destroy()

btn = tk.Button(text='Закрыть окно', command=close_window).pack()

root_book.mainloop()