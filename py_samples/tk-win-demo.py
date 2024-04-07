'''
    This is a Python3 app.

    Purpose: Demonstrate simple windows app powered by Tkinter.

    Usage: python3 tkwinapp.py

    IMPORTANT NOTICE:

        1.  Tkinter(Tk Gui Toolkit Interface) is shipped with Python official installer
            (Python Version 3.7 or above) as a standard Python package by default. 

        2.  If you cannot run this demo on debian/ubuntu/deepin linux platform OS properly, 
            or an error message like 'no module found...' showed up, you're able to install 
            'python3-tk' package on your platform by the command line below. 

            ***************************************
            *                                     *
            *   sudo apt-get install python3-tk   *
            *                                     *
            ***************************************

'''
import tkinter as tk
from tkinter import font, filedialog, messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tkinter Window App")
        self.master.geometry("960x320+100+100")
        self.master.resizable(0,0)
        self.pack(padx=64, pady=32)
        self.create_widgets()

    def create_widgets(self):
        self.work_zone = tk.Frame(self)
        self.work_zone.pack(side="top")

        self.operation_zone = tk.Frame(self)
        self.operation_zone.pack(side="bottom")

        self.choose_file = tk.Button(self.work_zone, bg="light gray", fg="#333", 
            activebackground="dark gray", activeforeground="white")
        self.choose_file["text"] = "Choose File"
        self.choose_file["command"] = self.chooseFile
        self.choose_file.pack(side="left", ipadx=10, padx=10, pady=50)

        self.open_file_label = tk.Label(self.work_zone)
        self.open_file_label.config(anchor="w", padx=10, bg="#CCC", fg="#666", width=65)
        self.open_file_label["text"] = "Filename will be shown here..."
        self.open_file_label.pack(side="right")

        self.process = tk.Button(self.operation_zone, text="PROCESS & OUTPUT FILE", 
            font=font.Font(weight="bold"), 
            bg="green", fg="yellow", 
            activebackground="dark green", activeforeground="white", 
            command=self.processFile)
        self.process.pack(side="left", ipadx=20, ipady=20, padx=50, pady=10)

        self.quit = tk.Button(self.operation_zone, text="QUIT", fg="red",
            command=self.master.destroy)
        self.quit.pack(side="right", ipadx=20, ipady=20, padx=50, pady=10)

    def chooseFile(self):
        filename = filedialog.askopenfilename()
        self.open_file_label["text"] = filename

    def processFile(self):
        print('Hi There, Start processing [{}] file...'.format(self.open_file_label["text"]))
        '''
            Add your codes here
        '''

        print("Done!")
        process_result = messagebox.showinfo(message="Work Finished!")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
