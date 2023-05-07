import sqlite3, datetime
import transport
from transport import * #импорт классов трансопрта

#---------------------- основные стартовые сведения организации  ---------------------------

# создададим основные объекты (транспорт в наличии у компании)
tr=[transport.Gazel(),
    transport.Bachok(),
    transport.Man_10(),
    transport.Fyra(),
    transport.Man_10(),
    transport.Gazel(),
    transport.Bachok(),
    transport.Man_10(),
]

# добавим некоторые заказанные машины
order=[(2198921,2,'Доставка мебели','23.05.2023','23.05.2023','12:00', '15:00','89813212'),
       (38931,7,'Перевоз вещей на новую квартиру в соседний город','21.05.2023','22.05.2023','12:00','09:00','Заказчик - ФИО'),
       (31781,1,'Доставка','30.05.2023','31.05.2023','04:00','08:00','wedew'),
       (383,4,'Переезд','04.05.2023','04.05.2023','16:00','18:00','wedw'),
       (1291,3,'Перевозка','08.05.2023','08.05.2023','08:00', '22:00','wed'),
        (6919,3,'','01.05.2023','09.05.2023','08:00', '22:00',''),
        (19291,2,'Доставка','10.05.2023','10.05.2023','10:00', '22:00','wdedew'),
        (9723,3,'','02.05.2023','02.05.2023','08:00', '09:00','qie'),
        (1321,1,'Секретно','02.05.2023','10.05.2023','08:00', '08:00',''),
        (331,4,'Для другой компании','13.05.2023','13.05.2023','12:00', '15:00','89-- номер ФИО'),
        (9013,3,'Аренда','17.05.2023','17.05.2023','02:00', '23:00',''),
        (314,8,'Перевозка','12.05.2023','12.05.2023','12:00', '13:00',''),
        (813,5,'Доставка, хрупко','10.05.2023','10.05.2023','08:00', '12:00','Позвонить заказчику перед доставкой'),
        (190,5,'Перевозка','26.05.2023','27.05.2023','08:00', '9:00','Доставка хрупкого, аккуратно!')
]

#---------------------------- создание таблиц ------------------------------

con = sqlite3.connect('pages/transport.db')

#для хранения основной информации о транспорте
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS transports (
           id_tr INTEGER PRIMARY KEY,
           type VARCHAR(30) NOT NULL,
           loadcapacity REAL NOT NULL,
           length REAL NOT NULL,
           width REAL NOT NULL,
           height REAL NOT NULL
);
    """)

# для хранения истории о загруженном и свободном транспорте
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS history (
           id INT PRIMARY KEY NOT NULL,
           id_tr INT NOT NULL,
           order_description VARCHAR(100),
           start_date VARCHAR(10) NOT NULL,
           end_date VARCHAR(10) NOT NULL,
           start_time VARCHAR(5),
           end_time VARCHAR(5),
           inf VARCHAR(100),
           FOREIGN KEY (id_tr) REFERENCES transport(id_tr) ON DELETE CASCADE
);
    """)

con.commit()

# добавляем с помощью множественного запроса все данные сразу
sql = 'INSERT INTO transports (type, loadcapacity, length, width, height) values( ?, ?, ?, ?, ?)'
with con:
    con.executemany(sql, [(tr[x].type,tr[x].loadcapacity,tr[x].length,tr[x].width,tr[x].height) for x in range(len(tr))])

sql = 'INSERT INTO history (id,id_tr, order_description, start_date, end_date, start_time, end_time,inf) values(?,?,?, ?, ?, ?, ?, ?)'
with con:
    con.executemany(sql, order)


