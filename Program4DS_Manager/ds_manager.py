import tkinter
from tkinter import ttk 
from tkinter import filedialog
from tkinter import *
import os

import distributed_system as ds

window=tkinter.Tk()
window.title("RS Manager")
window.geometry("600x300+100+100")

window.columnconfigure(index=0,weight=1)
window.columnconfigure(index=1,weight=1)
window.rowconfigure(index=0,weight=4)
window.rowconfigure(index=1,weight=1)



progects=[]
progects_var = Variable(value=progects)

ds.init()

def Destribute():
    dirpath=filedialog.askdirectory()
    arr=dirpath.split("/")
    progName=arr[len(arr)-1]
    file_names = []
    for file_name in os.listdir(dirpath):
        if os.path.isfile(os.path.join(dirpath, file_name)):
            file_names.append(f"{dirpath}/{file_name}")
    print(file_names)
    
    if(ds.checkIntegrity()):
        ds.sendFiles(progName,file_names)
    
    progects.append(progName)
    progects_var.set(progects)

    
def GetProgect():
    if(ds.checkIntegrity()):
        ds.getFiles(lb.get(lb.curselection()))
   


button=ttk.Button(text="Distribute",command=Destribute)
button.grid(column=0,row=1,padx=6,pady=6,sticky="NSEW")

button2=ttk.Button(text="Get Project",command=GetProgect)
button2.grid(column=1,row=1,padx=6,pady=6,sticky="NSEW")

lb=Listbox(listvariable=progects_var,selectmode=SINGLE,selectbackground="red")

lb.grid(column=0,columnspan=2,row=0,sticky="NSEW",padx=6,pady=6)


scroll=ttk.Scrollbar(orient="vertical",command=lb.yview)
scroll.grid(column=2,row=0,sticky="NS")
lb["yscrollcommand"]=scroll.set



window.mainloop()