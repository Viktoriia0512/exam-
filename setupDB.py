import sqlite3

conn=sqlite3.connect('student.db')
print("Opened database successfully")

conn.execute("""CREATE TABLE IF NOT EXISTS tblStudent(
        StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT,
        Address TEXT,
        City TEXT)""")
print("Table created succssfully")



conn=sqlite3.connect('course.db')
conn.execute("""CREATE TABLE IF NOT EXISTS tblCourse(
        courseID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        level INTEGER,
        courseDescription TEXT,
        credits INTEGER
)""")
conn.close()