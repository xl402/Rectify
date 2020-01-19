import tkinter as tk
import time
import pickle

def read_item_list():
    with open("item_list.pkl", "rb") as fp:   # Unpickling
        item_list = pickle.load(fp)

    recyclable_dict = {"apple": 0, "banana": 0, "orange":0, "water_bottle":1, "mixing_bowl":1}
    data_list = [[i, recyclable_dict[i]] for i in item_list]

    return(data_list)

def read_status():
    with open("status.txt", "rb") as f:
        text = f.read()
    return(text)


win = tk.Tk()
frame = tk.Frame(win)
frame.pack()

win.title("Our First GUI")
color_list = ["red", "green"]

while True:
    frame.destroy()
    print("destroying...")
    frame = tk.Frame(win)
    frame.pack()

    list = read_item_list()
    for i in range(len(list)):
        name = list[i][0]
        color = color_list[list[i][1]]
        tk.Label(frame, text=name, font=("Arial Bold", 50), fg=color).grid(row=i, column=0)

    status = read_status()
    tk.Label(frame, text=status, font=("Arial Bold", 20), bg="yellow", fg="black", relief="solid", borderwidth=1, width=30).grid(row=0, column=1)
    win.update()
    frame.after(3000)
