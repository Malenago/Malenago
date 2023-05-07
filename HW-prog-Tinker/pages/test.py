
from tkinter import *
import tkinter as ttk
import os


#------------------------- основные настройки --------------------------

root = Tk() # типа создает окошко (всегда надо)
root.title('...') # название окошка
root.geometry('100x100') # размер окна (можно менять, как хочется)
root.resizable(False, False) #фиксируем (нельзя будет менять размеры)

#------------------------ основная часть часть --------------------------

# текст
label = ttk.Label(text="...")
label.pack()


# функция для закрытия (польностью разрушает окно)
def close_window():
    root.destroy()

# переход между окнами
def do_saw():
    os.system('python3 .../...py')

# в зависимости от функции тут разные действия будут
btn = ttk.Button(text="...", command=close_window)
btn.pack()

# всегда пишем в конце
root.mainloop()
