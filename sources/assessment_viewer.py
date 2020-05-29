import logging
import os
import shutil

import subprocess
import sys
import tkinter as tk
import traceback

import Data_Capture_Assess
import lesson_list_assess
from tkinter import messagebox, ttk, filedialog

from gtts import gTTS
import threading




logger = logging.getLogger("MagicLogger")
file_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
db = file_root + os.path.sep + "MagicRoom.db"



class MagicAssessmentPrint(tk.Toplevel):
    def __init__(self,parent,lesson_id="",*args,**kwargs):
        super().__init__(parent, *args,**kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        s = ttk.Style(self)
        s.theme_use('clam')
        s.configure('Red.TLabelframe', background="gray27")
        s.configure('Red.TLabelframe.Label', font=('helvetica', 14, 'bold'))
        s.configure('Red.TLabelframe.Label', foreground="white")
        s.configure('Red.TLabelframe.Label', background="gray27")
        s.configure('Blue.TButton', background="steelblue", foreground="white")
        s.map('Blue.TButton', background=[('active', '!disabled', 'dark turquoise'), ('pressed', 'steelblue')],
              foreground=[('pressed', "white"), ('active', "white")])
        s.configure('TScrollbar', background="gray27", foreground="gray33")
        s.map('TScrollbar', background=[('active', '!disabled', 'gray33'), ('pressed', 'gray27')],
              foreground=[('pressed', "gray33"), ('active', "gray33")])
        self.configure(background="gray25")
        Data_Capture_Assess.db = db
        if lesson_id == "" or lesson_id is None:
            app = lesson_list_assess.MagicLessonList(parent=self)
            app.geometry("340x700+20+20")
            self.wait_window(app)
            print(self.selected_lessons)
            self.lesson_id = self.selected_lessons[0]
        else:
            self.lesson_id = lesson_id
        self.assessment_labelframe = ttk.Labelframe(self,text="Generate Assessment",style="Red.TLabelframe")

        self.assessment_PDF_label = ttk.Label(self.assessment_labelframe , text="View Assessment File",style="Red.TLabelframe.Label")
        self.assessment_PDF_Button = ttk.Button(self.assessment_labelframe ,text="View", command=self.display_PDF,style="Blue.TButton")
        self.assessment_PDF_label.grid(row=0,column=0,padx=5,sticky=tk.W)
        self.assessment_PDF_Button.grid(row=0,column=1)
        assessment_text = Data_Capture_Assess.get_Assessment_Text(self.lesson_id)
        assessment_file = file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(self.lesson_id)+os.path.sep+"audio_assessment_"+str(self.lesson_id)+".mp3"
        self.audio_button = ttk.Button(self.assessment_labelframe , text="Generate",
                                       command=lambda: self.generate_assessment_audio(assessment_text, self.lesson_id),style="Blue.TButton")
        self.audio_label = ttk.Label(self.assessment_labelframe ,text="Generate Audio Assessment",style="Red.TLabelframe.Label")
        self.audio_label.grid(row=1, padx=5,column=0,sticky=tk.W)
        self.audio_button.grid(row=1,padx=5, column=1)
        if (os.path.exists(assessment_file)):
                self.audio_play_label = ttk.Label(self.assessment_labelframe ,text="Play Existing Assessment Audio",style="Red.TLabelframe.Label")
                self.audio_play_button = ttk.Button(self.assessment_labelframe , text="Play",
                                        command=lambda: self.play_assessment_audio(self.lesson_id),style="Blue.TButton")
                self.audio_play_label.grid(padx=5,row=2,column=0,sticky=tk.W)
                self.audio_play_button.grid(row=2,padx=5, column=1)
        self.assessment_labelframe.grid(row=0,column=0,padx=10,pady=10)

        self.save_audio_button = ttk.Button(self.assessment_labelframe, text="Save",
                                   command=lambda: self.save_assessment_audio(assessment_file, self.lesson_id),
                                   style="Blue.TButton")
        assessment_paper_file = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
            self.lesson_id) + os.path.sep + "ip_" + str(self.lesson_id) + ".pdf"
        self.save_file_button = ttk.Button(self.assessment_labelframe, text="Save",
                                   command=lambda: self.save_assessment_file(assessment_paper_file, self.lesson_id),
                                   style="Blue.TButton")
        self.notes_condition_label = ttk.Label(self, text="Audio assessment generation requires internet connectivity"
                                               , background="gray27", foreground="aquamarine",
                                               font=("helvetica", 10, "bold"))

        self.save_file_button.grid(row=0,column=2,padx=5,pady=8)
        self.save_audio_button.grid(row=1, column=2,padx=5,pady=8)
        self.notes_condition_label.grid(row=2, column=0)


    def display_PDF(self):
        self.assessment_paper_file = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
            self.lesson_id) + os.path.sep + "ip_" + str(self.lesson_id) + ".pdf"
        print(self.assessment_paper_file)
        messagebox.showinfo("File Opened",
                            "File will be opened in another window.\n\nAdobe File Reader is required to view the file.\n\nPlease save the file in your preferred location",parent=self)
        try:
            if sys.platform == "win32":
                os.startfile(self.assessment_paper_file)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, self.assessment_paper_file])
        except:
            messagebox.showerror("File open Error",
                                 "File could not be opened. Check if you have Adobe Reader Installed or if the folder has full permissions")
            logger.exception("File open error")

    # self.destroy()

    def generate_assessment_audio(self,text,lesson_id):
        start_audio = threading.Thread(target=self.generate_audio,args=(lesson_id,text))
        start_audio.start()
        messagebox.showinfo("Staus", "Online audio generation triggered.\n Player will start once generation is complete",parent=self)
        start_audio.join(20)

        if sys.platform == "win32":
            os.startfile(file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(lesson_id)+os.path.sep+"audio_assessment_"+str(lesson_id)+".mp3")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(lesson_id)+os.path.sep+"audio_assessment_"+str(lesson_id)+".mp3"
        ])

    def generate_audio(self, lesson_id, text):
        try:
            audio_object = gTTS(text=text, lang="en", slow=False)
            filepath = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                lesson_id) + os.path.sep + "audio_assessment_" + str(lesson_id) + ".mp3"
            print(filepath)
            audio_object.save(filepath)
        except:
            messagebox.showerror("Audio File Error", "Could not generate the audio file",parent=self)
            print("could not generate the audio file")
            logger.exception("Could not generate the audio file")

    def play_assessment_audio(self, lesson_id):

         try:
            if sys.platform == "win32":
                os.startfile(file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                    lesson_id) + os.path.sep + "audio_assessment_" + str(lesson_id) + ".mp3")
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(lesson_id)+os.path.sep+"audio_assessment_"+str(lesson_id)+".mp3"
             ])
         except:
               messagebox.showwarning("File Play Error","File could not be played",parent=self)
               logger.exception("Could not play the audio file")
    def save_assessment_audio(self, assessment_file, lesson_id):
        try:
            filename = filedialog.askdirectory(parent=self)
            shutil.copyfile(assessment_file,filename+os.path.sep+"assessment"+str(lesson_id)+".mp3")
            messagebox.showinfo("File Copy","File copied",parent=self)
        except:
            messagebox.showwarning("File Save Error","File could not be copied",parent=self)
            logger.exception("Could not copy the file")

    def save_assessment_file(self, assessment_file, lesson_id):
        try:
            filename = filedialog.askdirectory(parent=self)
            shutil.copyfile(assessment_file,filename+os.path.sep+"assessment"+str(lesson_id)+".pdf")
            messagebox.showinfo("File Copy","File copied",parent=self)
        except:
            messagebox.showwarning("File Save Error","File could not be copied",parent=self)
            logger.exception("Could not copy the file")


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
