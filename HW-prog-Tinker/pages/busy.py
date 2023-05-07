from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import Calendar
import datetime


#------------------------- функции вспомогательные ---------------------------

# перевод даты в нужный формат
def dates(dt):
        return [int(dt[6:]), int(dt[3:5]), int(dt[0:2])]


#------------------------- основные настройки --------------------------

root_busy = Tk()
root_busy.title('logistics-busy') #название
root_busy.geometry('750x700') #размер окна
root_busy.resizable(False, False) #фиксируем
font = ("LKLUG", 14) #шрифт

# ------------------------- база данных ---------------------------

def datbas(data=[2023, 5, 12]):
    
    # для сохранения загруженности транспорта
    tr_busy = []
    tr_busy_num = []
    tr_free=[]

    # подключаемся к БД, берем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """SELECT * from history"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    # определяем загруженность для конкретного выбранного дня
    for row in records:
        f_1 = dates(row[3])
        f_2 = dates(row[4])
        if datetime.datetime(f_1[0], f_1[1], f_1[2]) <= datetime.datetime(data[0], data[1], data[2]) \
                and datetime.datetime(data[0], data[1], data[2]) <= datetime.datetime(f_2[0], f_2[1], f_2[2]):
            tr_busy.append(row)
            tr_busy_num.append(row[1])

    # выбор айдишек доступного трансопрта для отбор
    sqlite_select_query = """SELECT id_tr from transports"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    # выбор свободного транспорта
    dat="{0:02d}.{1:02d}.{2}".format(data[2],data[1],data[0])
    for id_tr in records:
        if id_tr[0] not in tr_busy_num:
            tr_free.append(['-',id_tr,'-',dat,dat,'-','-'])
        else:
            tr_free.append(['-', id_tr, f'Занятость в этот день имеется!', dat, dat, '-', '-'])

    cursor.close()
    sqlite_connection.close()

    return tr_busy,tr_free

#------------------------ основная часть часть --------------------------

# текст в шапке
label = tk.Label(text="Занятость транспорта",
                  pady=20,font=("LKLUG", 22),fg="#1e1d52")
label.pack()

# выбор даты
label = tk.Label(text="Выберите дату:",
                  pady=5,font=("LKLUG", 15),fg="#1e1d52")
label.pack()

# календадрь для выбора даты
cal = Calendar(root_busy, selectmode='day', selectforeground='#4b9c74',
               foreground='#4b9c74',
               year=2023, month=5,
               day=15)

cal.pack(pady=5)

# функции для обновления данных в таблице
def get_1():
    label.config(text="Свободный транспорт на " + cal.get_date(),font=("LKLUG", 15),fg="#1e1d52")
    tab=datbas(dates(cal.get_date()))

    tree1.delete(*tree1.get_children())

    for x in tab[1]:
        tree1.insert("", END, values=x)


def get_2():
    label.config(text="Занятый транспорт на " + cal.get_date(),font=("LKLUG", 15),fg="#1e1d52")
    tab = datbas(dates(cal.get_date()))

    tree1.delete(*tree1.get_children())

    for x in tab[0]:
        tree1.insert("", END, values=x)


# кнопка для обновления данных
Button(root_busy, text="Показать свободный транспорт",
       command=get_1).pack(pady=5)

Button(root_busy, text="Показать занятый транспорт",
       command=get_2).pack(pady=5)

#-------------------- основная часть часть (таблица)  -------------------------


# текст
label = Label(root_busy, text = "")
label.pack()

# определяем столбцы
columns1 = ("id","id_tr", "description", "start_date","end_date","start_time","end_time")

tree1 = ttk.Treeview(columns=columns1, show="headings")
tree1.pack(padx=10,pady=20)

# определяем заголовки
tree1.heading("id", text="Номер доставки")
tree1.heading("id_tr", text="ВН транспорта")
tree1.heading("description", text="Описание")
tree1.heading("start_date",text="День - начало")
tree1.heading("end_date",text="День - конец")
tree1.heading("start_time",text="Время - начало")
tree1.heading("end_time",text="Время - конец")

# настройки
tree1.column("#1", stretch=NO, width=100,anchor ='c')
tree1.column("#2", stretch=NO, width=100,anchor ='c')
tree1.column("#3", stretch=NO, width=260,anchor ='c')
tree1.column("#4", stretch=NO, width=90,anchor ='c')
tree1.column("#5", stretch=NO, width=90,anchor ='c')
tree1.column("#6", stretch=NO, width=90,anchor ='c')
tree1.column("#7", stretch=NO, width=90,anchor ='c')



# функция для закрытия окна
def close_window():
    root_busy.destroy()

btn = tk.Button(text='Закрыть окно', command=close_window).pack()


root_busy.mainloop()

