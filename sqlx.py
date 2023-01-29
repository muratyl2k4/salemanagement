import sqlite3

db = sqlite3.connect('example2.db')     

cursor = db.cursor()   
query = '''create table person (
    id        INTEGER primary key,
    firstname        text,
    lastname        text,
    age             INTEGER
)'''