import configparser
import os
import sqlite3
from tkinter import messagebox
from pathlib import Path

file_root = os.path.abspath(os.path.join(os.getcwd(),".."))
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

def get_Assessment_Text(lesson_id):
    print (db)
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select IP_Questions from Magic_Science_Lessons where Lesson_ID=?"
    cur.execute(sql,(lesson_id,))
    rows = cur.fetchall()
    text = rows[0]
    connection.commit()
    connection.close()
    return text[0]



