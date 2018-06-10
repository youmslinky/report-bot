import sqlite3
import time


conn = sqlite3.connect('pic_links.db')
c = conn.cursor()

fp = open("waifu_links")
lines = fp.readlines()
n=0
for l in lines:
    c.execute("INSERT INTO waifus(link,   unixTimeAdded,    viewNumber) VALUES (?,?,?)", (str(l),int(time.time()), 0))

conn.commit()