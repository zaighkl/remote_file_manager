import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
from tkinter import *

import client
from client import *


parent = ttk.Window(themename ="darkly")

def send_file_name_to_user():
    lb = parent.nametowidget('dwn.lb')
    selected_idx = lb.curselection()
    file_name = lb.get(selected_idx)
    child3 = tk.Toplevel(parent)
    child3.grab_set()
    child3.title("Remote file manager")
    child3.geometry("600x400")
    title_label = ttk.Label(master=child3, text="Remote file manager", font="Georgia 24 bold")
    title_label.pack()
    button = Button(master=child3, text="OK", command=child3.destroy)
    button.pack()
    title_label.pack()
    if client.download(file_name):
        title = ttk.Label(master = child3, text="downloaded successfully!!!", font="Georgia 10")
    else:
        title = ttk.Label(master=child3, text="seems like there was a problem, the file wasn't downloaded :(((", font="Georgia 10")
    title.pack()

def fileselector():
    path = fd.askopenfilename()
    child4 = tk.Toplevel(parent)
    child4.grab_set()
    child4.title("Remote file manager")
    child4.geometry("600x400")
    title_label = ttk.Label(master=child4, text="Remote file manager", font="Georgia 24 bold")
    title_label.pack()
    button = Button(master=child4, text="OK", command=child4.destroy)
    button.pack()
    title_label.pack()

    if client.upload(path):
        title = ttk.Label(master=child4, text="Uploaded succeesfully!!", font="Georgia 10")
    else:
        title = ttk.Label(master=child4, text="seems like there was a problem, the file wasn't uploaded :(", font="Georgia 10")
    title.pack()


def upload():

    child1 = tk.Toplevel( parent )
    child1.title("Remote file manager")
    child1.geometry("600x400")
    title_label = ttk.Label(master = child1, text = "Remote file manager", font = "Georgia 24 bold")
    title_label.pack()
    title = ttk.Label(master = child1, text = "which file do you want to upload", font = "Georgia 10")
    title_label.pack()
    title.pack()
    button1 = ttk.Button(master = child1, text = "chose file"  , command = fileselector)
    button1.pack(pady = '20px')

    child1.mainloop()

def download():

    file_names = get_file_names()
    child2 = tk.Toplevel(parent, name="dwn")
    child2.title("Remote file manager")
    child2.geometry("600x400")
    title_label = ttk.Label(master=child2, text="Remote file manager", font="Georgia 24 bold")
    title_label.pack()
    title = ttk.Label(master=child2, text="which file do you want to download", font="Georgia 10")
    title.pack()
    listbox = Listbox(name='lb', master = child2, width=30, height=10, selectmode = SINGLE)
    for i in range(len(file_names)):
        listbox.insert(i+1,file_names[i])

    for i in listbox.curselection():
        print(listbox.get(i))
    listbox.pack()
    btn =  ttk.Button(master = child2, text="Download", command = send_file_name_to_user )
    btn.pack()


def main_window():
    parent.title("Remote file manager")
    title_label = ttk.Label(master = parent, text ="Remote file manager", font ="Georgia 24 bold")
    title_label.pack()
    title = ttk.Label(master = parent, text ="what do you want to do?", font ="Georgia 10")
    title.pack(pady='10px')
    parent.geometry("600x400")  # x and y

    frame_input = ttk.Frame(master=parent)
    button1 = ttk.Button(master = frame_input, text="Upload", command = upload)
    button1.pack(side = "right", padx="20px")
    button2 = ttk.Button(master = frame_input, text="Download", command = download)
    button2.pack(side = "right", padx="20px")
    frame_input.pack(pady="30px")
    parent.mainloop()

main_window()