import sqlite3

conn=sqlite3.connect('login.db')

conn.execute("""CREATE TABLE IF NOT EXISTS tblLogin(
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)""")
conn.execute('insert into tblLogin (userID, email, password) VALUES (120,"xyz@mail.com", "123xyz")')
conn.execute('insert into tblLogin (email,password) VALUES ("abc@mail.com", "123abc")')

conn.commit()
