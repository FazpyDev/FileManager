import os
from customtkinter import *
from PIL import Image
import win32api
import win32con
import ctypes
from tkinter import filedialog
#VARIABLES  

FILE_ATTRIBUTE_HIDDEN = 0x2

width = 1600
height = 900
defPath = r"C:\Users\coded"

currentPath = defPath

app = CTk()
app.geometry(f"{width}x{height}")

app.grid_rowconfigure(0, weight=1)    
app.grid_columnconfigure(0, weight=1)  
app.grid_columnconfigure(1, weight=0)  
Icon = "Assets/FolderIcon.png"

MainFrame = CTkScrollableFrame(master=app, width=1300, height=height, fg_color="#131313")
MainFrame.grid(row=0, column=9, sticky="nsew")#
MainFrame.grid_columnconfigure(0, weight=1)
MainFrame.grid_rowconfigure(0, weight=1)

def OpenPath():
    global currentPath
    currentPath = filedialog.askdirectory(initialdir=currentPath,
                                          title="Please select a Folder to open",
    )
    PathTextBox.delete(0, "end")
    PathTextBox.insert(0, currentPath)
    for widget in MainFrame.winfo_children():
        widget.destroy()
    LoadFiles(currentPath)

def openPathEntryBox():
    value = PathTextBox.get()
    if os.path.isdir(value):
        currentPath = value
        for widget in MainFrame.winfo_children():
            widget.destroy()
        LoadFiles(currentPath)

PathTextBox = CTkEntry(master=app, placeholder_text=f"{currentPath}", height=50, fg_color="#181818")
PathTextBox.grid(row=0, column=0, sticky="nwe")
SelectFileBtn = CTkButton(master=app, text="Open", height=50, width=10, fg_color="#222222", hover_color="#141414", command=OpenPath)
SelectFileBtn.grid(row=0, column=0, sticky="ne", padx=(0, 40))
EnterBtn = CTkButton(master=app, text="Enter", height=50, width=10, fg_color="#222222", hover_color="#141414", command=openPathEntryBox)
EnterBtn.grid(row=0, column=0, sticky="ne")

#Important Directories
DesktopBtn = CTkButton(master=app, text="Desktop")
DesktopBtn.grid(row=2, column=0)

def is_hidden(filepath):
    attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
    return attrs != -1 and (attrs & FILE_ATTRIBUTE_HIDDEN)

def CreateFile(Directory, i, file):
    path = os.path.join(Directory, file)
    if not is_hidden(path):
                

        FileFrame= CTkFrame(master=MainFrame, width=1000, bg_color="#202020", )
        FileFrame.grid_columnconfigure(1, weight=1)
        FileFrame.grid(row=i+1, column=0, pady=10)

        hiddenLabel = CTkLabel(master=FileFrame, width=5200, text="") #Dont mind this
        hiddenLabel.grid(row=1, column=3)

        FolderImage = CTkImage(light_image=Image.open(Icon), size=(100, 100))
        FileFrame.FileImageLabel = CTkLabel(master=FileFrame, text="",height=100, width=100)
        FileFrame.FileImageLabel.grid(row=1, column=0)

        
        def OpenFile():
            if os.path.isdir(os.path.join(Directory, FileFrame.FileName._text)):
                global currentPath
                currentPath = os.path.join(Directory, file)
                
                PathTextBox.delete(0, "end")
                PathTextBox.insert(0, currentPath)
                for widget in MainFrame.winfo_children():
                    widget.destroy()
                LoadFiles(currentPath)
            else:
                os.startfile(path)

        def DeleteFile():
            if os.path.exists(path):
                os.remove(path)
                LoadFiles(currentPath)

        OpenBtn = CTkButton(master=FileFrame, text="Open", command=OpenFile, fg_color="#252525")
        OpenBtn.place(relx=0.8, rely=0.5, anchor="center")

        DeleteBtn = CTkButton(master=FileFrame, text="Delete", command=DeleteFile, fg_color="#252525")
        DeleteBtn.place(relx=0.9, rely=0.5, anchor="center")

        FileFrame.FileName = CTkLabel(master=FileFrame, width=200, height=50, text=file, font=("Arial", 20))
        FileFrame.FileName.grid(row=1, column=2)



        if os.path.isdir(path):
            FileFrame.FileImageLabel.configure(image=FolderImage)

def LoadFiles(Directory):
    for i, file in enumerate(os.listdir(Directory)):
      CreateFile(Directory, i, file)

LoadFiles(currentPath)
app.mainloop()   