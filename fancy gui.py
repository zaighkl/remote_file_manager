import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
from tkinter import *

import client
from client import *

parent = ttk.Window(themename ="darkly")

def send_file_to_user():
    child3 = tk.Toplevel(parent)
    child3.title("Remote file manager")
    child3.geometry("600x400")
    title_label = ttk.Label(master=child3, text="Remote file manager", font="Georgia 24 bold")
    title_label.pack()
    title = ttk.Label(master=child3, text="ur mom", font="Georgia 10")
    title_label.pack()
    title.pack()

def fileselector():
    server_socket = client.get_server_socket()
    file_name = fd.askopenfilename()
    send_to_server(server_socket, file_name, True)

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
    server_socket = client.get_server_socket()
    file_names = get_file_names(server_socket)

    child2 = tk.Toplevel(parent)
    child2.title("Remote file manager")
    child2.geometry("600x400")
    title_label = ttk.Label(master=child2, text="Remote file manager", font="Georgia 24 bold")
    title_label.pack()
    title = ttk.Label(master=child2, text="which file do you want to download", font="Georgia 10")
    title.pack()
    listbox = Listbox(master = child2, width=30, height=10, selectmode = SINGLE)
    for i in range(len(file_names)):
        listbox.insert(i+1,file_names[i])

    for i in listbox.curselection():
        print(listbox.get(i))
    listbox.pack()
    btn =  ttk.Button(master = child2, text="Upload", command = send_file_to_user)
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