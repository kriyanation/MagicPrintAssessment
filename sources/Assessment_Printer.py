import configparser
import os
import sqlite3
import subprocess
import sys
import tkinter as tk

import Data_Capture
import LessonList
from tkinter import messagebox
from reportlab.pdfgen import canvas
from pathlib import Path

config = configparser.RawConfigParser()
two_up = Path(__file__).parents[2]
try:
    config.read(str(two_up)+'/magic.cfg')
    file_root = config.get("section1", 'file_root')
    db = file_root+os.path.sep+'MagicRoom.db'
    print(db)

except configparser.NoSectionError:
    messagebox.showerror("Configuration Error", "No Section found or Configuration File Missing")
    sys.exit()

class MagicAssessmentPrint(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent, *args,**kwargs)
        Data_Capture.db = db
        app = LessonList.MagicLessonList(bg='beige', fg='firebrick', buttonbg='firebrick', selectmode=tk.SINGLE,
                              buttonfg='snow',parent=self)

        self.wait_window(app)
        print(self.selected_lessons)
        self.lesson_id = int(self.selected_lessons[0:self.selected_lessons.index(':')-1].strip())


        self.assessment_paper_file = file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(self.lesson_id)+os.path.sep+"papers"+os.path.sep+"ip_"+str(self.lesson_id)+".pdf"
        print(self.assessment_paper_file)
        messagebox.showinfo("File Opened", "File is opened in another window. Adobe File Reader is required to view the file.\n Please save the file in your preferred location")
        try:
            if sys.platform == "win32":
                os.startfile(self.assessment_paper_file )
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, self.assessment_paper_file])
        except:
            messagebox.showerror("File open Error","File could not be opened. Check if you have Adobe Reader Installed or if the folder has full permissions")


if __name__== "__main__":
    dashboard_app = tk.Tk()
    dashboard_app.configure(background="gray25")
    dashboard_app.title("Learning Room Assessment")
    dashboard_app.geometry("800x800")
    frame = MagicAssessmentPrint(dashboard_app)
    #dashboard_app.rowconfigure(0,weight=1)
    dashboard_app.columnconfigure(0, weight=1)
    frame.grid(row=0,column=0)
    dashboard_app.mainloop()
