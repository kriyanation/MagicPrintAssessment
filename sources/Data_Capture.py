import configparser
import os
import sqlite3
from tkinter import messagebox
from pathlib import Path

config = configparser.RawConfigParser()
two_up = Path(__file__).absolute().parents[2]
print(str(two_up)+'/magic.cfg')
config.read(str(two_up)+'/magic.cfg')
file_root = config.get("section1",'file_root')
db = file_root+os.path.sep+"MagicRoom.db"

def get_Lessons():
    print (db)
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_ID, Lesson_Title from Magic_Science_Lessons"
    cur.execute(sql)
    rows = cur.fetchall()
    list_lessons = []
    for element in rows:
        list_lessons.append(element)
    connection.commit()
    connection.close()
    return list_lessons


