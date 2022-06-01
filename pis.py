import sqlite3


import sqlite3

#just a checking program

con = sqlite3.connect('zoo.db')

c = con.cursor()

c.execute("SELECT * FROM zvierata")

for i in c.fetchall():
    print(i)

c.execute("SELECT * FROM pracovnici")

for i in c.fetchall():
    print(i)