
import os

import subprocess
import sys
import tkinter as tk

import Data_Capture_Assess
import lesson_list_assess
from tkinter import messagebox


file_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
db = file_root + os.path.sep + "MagicRoom.db"



class MagicAssessmentPrint(tk.Toplevel):
    def __init__(self,parent,lesson_id="",*args,**kwargs):
        super().__init__(parent, *args,**kwargs)
        self.configure(background="gray16")
        Data_Capture_Assess.db = db
        if lesson_id == "" or lesson_id is None:
            app = lesson_list_assess.MagicLessonList(bg='beige', fg='firebrick', buttonbg='firebrick', selectmode=tk.SINGLE,
                                                     buttonfg='snow', parent=self)

            self.wait_window(app)
            print(self.selected_lessons)
            self.lesson_id = int(self.selected_lessons[0:self.selected_lessons.index(':')-1].strip())
        else:
            self.lesson_id = lesson_id


        self.assessment_paper_file = file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(self.lesson_id)+os.path.sep+"ip_"+str(self.lesson_id)+".pdf"
        print(self.assessment_paper_file)
        messagebox.showinfo("File Opened", "File will be opened in another window.\n\nAdobe File Reader is required to view the file.\n\nPlease save the file in your preferred location")
        try:
            if sys.platform == "win32":
                os.startfile(self.assessment_paper_file )
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, self.assessment_paper_file])
        except:
            messagebox.showerror("File open Error","File could not be opened. Check if you have Adobe Reader Installed or if the folder has full permissions")
        self.destroy()

#if __name__== "__main__":
    # dashboard_app = tk.Tk()
    # dashboard_app.configure(background="gray25")
    # dashboard_app.title("Learning Room Assessment")
    # dashboard_app.geometry("800x800")
    # frame = MagicAssessmentPrint(dashboard_app)
    # #dashboard_app.rowconfigure(0,weight=1)
    # dashboard_app.columnconfigure(0, weight=1)
    # frame.grid(row=0,column=0)
    # dashboard_app.mainloop()
