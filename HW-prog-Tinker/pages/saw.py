from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox


#------------------------- функции вспомогательные ---------------------------

# функции для обновления данных в таблице
def get():
    tab=datbas()

    tree1.delete(*tree1.get_children())

    for x in tab[0]:
        tree1.insert("", END, values=x)

#------------------------- база данных ---------------------------

# выбирает все данные по транспорту, а также отдельно айди
def datbas():

    # для сохранения информации
    list=[]
    id_tr=[]

    # подключаемся к БД, берем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """SELECT * from transports"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    #считаем все айдишки транспорта в наличии у компании
    id_tr=[x[0] for x in records]

    cursor.close()
    sqlite_connection.close()

    return records,id_tr


# удаляет транспорт по выбранному пользователем айди
def del_id(id):

    # подключаемся к БД, берем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """DELETE from transports WHERE id_tr = ?"""
    cursor.execute(sqlite_select_query, (id,))
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()

    get()


# выбирает данные из БД и сортирует по ГП, потом выводит в таблицу (в БД не сохраняет)
def sort_bd_1():

    # подключаемся к БД, берем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """SELECT * from transports ORDER BY loadcapacity"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    tree1.delete(*tree1.get_children())

    for x in records:
        tree1.insert("", END, values=x)

    cursor.close()
    sqlite_connection.close()

def sort_bd_2():

    # подключаемся к БД, берем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """SELECT * from transports ORDER BY loadcapacity DESC"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    tree1.delete(*tree1.get_children())

    for x in records:
        tree1.insert("", END, values=x)

    cursor.close()
    sqlite_connection.close()

# добавление в БД
def add_db(mas):

    # подключаемся к БД, обновляем данные
    sqlite_connection = sqlite3.connect('pages/transport.db')
    cursor = sqlite_connection.cursor()

    sqlite_insert_with_param = """INSERT INTO transports
                                  (type, loadcapacity, length, width, height) 
                                  VALUES( ?, ?, ?, ?, ?);"""

    data_tuple = (mas[0], mas[1], mas[2], mas[3], mas[4])
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()

    get()


#------------------------- основные настройки --------------------------

root_saw = Tk()
root_saw.title('logistics-saw') #название
root_saw.geometry('750x750') #размер окна
root_saw.resizable(False, False) #фиксируем
font = ("LKLUG", 14) #шрифт


#------------------------ основная часть часть --------------------------

# текст в шапке
label = tk.Label(text="Просмотр и редактирование транспорта",
                  pady=10,font=("LKLUG", 22),fg="#1e1d52")
label.pack()


#-------------------- основная часть часть (таблица)  -------------------------

# текст
label = Label(root_saw, text = "")
label.pack()

# определяем столбцы
columns1 = ("id_tr", "type", "loadcapacity","length","width","height")

tree1 = ttk.Treeview(columns=columns1, show="headings")
tree1.pack()

# определяем заголовки
tree1.heading("id_tr", text="ВН транспорта")
tree1.heading("type", text="Тип")
tree1.heading("loadcapacity",text="Грузоподъемность")
tree1.heading("length",text="Длина")
tree1.heading("width",text="Ширина")
tree1.heading("height",text="Высота")

# настройки
tree1.column("#1", stretch=NO, width=100,anchor ='c')
tree1.column("#2", stretch=NO, width=100,anchor ='c')
tree1.column("#3", stretch=NO, width=140,anchor ='c')
tree1.column("#4", stretch=NO, width=90,anchor ='c')
tree1.column("#5", stretch=NO, width=90,anchor ='c')
tree1.column("#6", stretch=NO, width=90,anchor ='c')

# вставка данных из БД
DB=datbas()
get()

#-------------------- основная часть часть (удаление)  -------------------------

# функция, проверяющая ввод айди и напрвляющая на удаление
def del_f():
    id = id_del_entry.get()
    print(id,DB[1])
    tab=[str(x) for x in DB[1]]
    if id not in tab:
        messagebox.showinfo('Сообщение','Повторите ввод, такого внутреннего номера транспорта (ВН) нет в базе!')
    else:
        del_id(id)
        messagebox.showinfo('Сообщение', 'Удаление выполнено успешно!')


# удаление
label = tk.Label(text="Выберите ВН транспорта для удаления",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack()

# поле ввода
id_del_entry = Entry(root_saw)
id_del_entry.pack()

# кнопка
Button(root_saw, text='Удалить', command=del_f).pack(pady=5)

#-------------------- основная часть часть (просмотр)  -------------------------


# просматривать грузовой транспорт по грузоподъемности

label = tk.Label(text="Просмотр транспорта по грузоподъемности",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack()

# кнопки для сортировки
Button(root_saw, text="По возрастанию",command=sort_bd_1).pack()
Button(root_saw, text="По убыванию",command=sort_bd_2).pack()

#-------------------- основная часть часть (добавление)  -------------------------

# добавление данных с проверкой
def add_f():
    tp=name_entry.get()
    ld=loadcapacity_entry.get()
    lg=length_entry.get()
    wd=width_entry.get()
    hg=height_entry.get()

    s='0123456789.'
    if all(x in s for x in ld) and \
       all(x in s for x in lg) and \
       all(x in s for x in wd) and \
       all(x in s for x in hg) and \
       len(tp)<=30:
        add_db([tp, ld, lg, wd, hg])
        messagebox.showinfo('Сообщение', 'Данные были успешно занесены!')
    else:
        messagebox.showerror('Сообщение', 'Ошибка в вводе данных! Повторите снова')



# добавление
label = tk.Label(text="Добавление нового транспорта",
                  font=("LKLUG", 15),fg="#1e1d52")
label.pack()


label_name = tk.Label(text="Тип:").place(x=260,y=480)
name_entry = Entry(root_saw)
name_entry.place(x=350,y=480)

loadcapacity = tk.Label(text="Грузо-ть:").place(x=260,y=520)
loadcapacity_entry = Entry(root_saw)
loadcapacity_entry.place(x=350,y=520)

length = tk.Label(text="Длина:").place(x=260,y=560)
length_entry = Entry(root_saw)
length_entry.place(x=350,y=560)

width_name = tk.Label(text="Ширина:").place(x=260,y=600)
width_entry = Entry(root_saw)
width_entry.place(x=350,y=600)

height_name = tk.Label(text="Высота:").place(x=260,y=640)
height_entry = Entry(root_saw)
height_entry.place(x=350,y=640)

# кнопка отправки формы
Button(root_saw, text='Добавить', command=add_f).place(x=330,y=670)


# функция для закрытия окна
def close_window():
    root_saw.destroy()

btn = tk.Button(text='Закрыть окно', command=close_window).place(x=320,y=700)

root_saw.mainloop()




