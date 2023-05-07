import sqlite3

#---------------------------- создание таблиц ------------------------------

con = sqlite3.connect('applications.db')

#для хранения основной информации о транспорте
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS applications (
           id INTEGER PRIMARY KEY,
           first_name VARCHAR(100) NOT NULL,
           last_name VARCHAR(100) NOT NULL,
           loadcapacity REAL NOT NULL,
           length REAL NOT NULL,
           width REAL NOT NULL,
           height REAL NOT NULL,
           information VARCHAR(200)
);
    """)

con.commit()


