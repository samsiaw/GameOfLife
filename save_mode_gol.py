"""@author: Samuel T. Siaw
Date: 10th August, 2020.
Final Class: Design of window for Conway's Game of Life completed on 8th August
Main game algorithm and tweaking finished on 9th August, 2020."""

import csv
from tkinter import messagebox
from tkinter import simpledialog

#import canvas_outline as game

def save(live_cells, canvas_width, canvas_height):
    with open(file= "save.csv", mode= "a") as file:
        writer = csv.writer(file)
        filename = simpledialog.askstring(title= "Filename", prompt="Input name for file:")
        writer.writerow((filename.lower(),canvas_width,canvas_height, [l for l in live_cells]))
        messagebox.showinfo("Done", "Pattern saved successfully.")

def read_file(canvas_width, canvas_height):
    from collections import defaultdict
    file_text = defaultdict(list)
    with open(file= "save.csv", mode = "r") as file:
        reader = csv.reader(file)
        """Show message with current files' names and ask for which to select.
        Return the list for the selected one."""
        for line in reader:
            if line!= []:
                file_text["name"].append(line[0])
                file_text["canv_w"].append(line[1])
                file_text["canv_h"].append(line[2])
                file_text["cells"].append(line[3])
            print("end")
    dialog_string = ""
    if len(file_text["name"])==0:
        dialog_string = "No files saved"
    else:
        n = 1
        for i in range(1,len(file_text["name"])+1):
            dialog_string += f"{n}. {file_text['name'][n-1]}\n"
            n += 1

    num_savedfile = simpledialog.askinteger(title = "Load Saved File",prompt= "Input number of saved file here:\n" +dialog_string)

    if canvas_width == int(file_text["canv_w"][num_savedfile-1]) and canvas_height == int(file_text["canv_h"][num_savedfile-1]):
        return file_text["cells"][num_savedfile-1]
    else:
        messagebox.showerror("Cannot Load Save File", "Current Canvas Width and Height is incompatible with saved file's stored values.\nChoose another.")
        return False







