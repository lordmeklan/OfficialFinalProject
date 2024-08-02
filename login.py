import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL ,
    password VARCHAR(255) NOT NULL
)
""")

username1, password1 = "mike123" , hashlib.sha256("mikepassword".encode()).hexdigest()
username2, password2 = "john" , hashlib.sha256("johnjohn".encode()).hexdigest()
username3, password3 = "manman" , hashlib.sha256("thugman12".encode()).hexdigest()
username4, password4 = "jerry" , hashlib.sha256("jerryspringer".encode()).hexdigest()
username5, password5 = "Perrytim" , hashlib.sha256("TheUknown".encode()).hexdigest()

cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)",(username1, password1))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)",(username2, password2))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)",(username3, password3))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)",(username4, password4))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)",(username5, password5))

conn.commit()