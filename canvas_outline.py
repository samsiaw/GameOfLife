"""Conway's Game of Life Simulation
Started: August 6th 2020
@author: Samuel T. Siaw"""

# Objective: Draw a canvas
# Draw grids on the canvas to represent cells
# Mouse click on a cell highlights the cell

from tkinter import *
from tkinter import ttk
from gol_algo import GameOfLife as gol
from Constants import constants as const
from random import randint
from tkinter import font as tkFont
import save_mode_gol as save

class Canvas_design(object):
    def __init__(self, master):

        self.root = master
        self.root.title("Conway's Game of life")
        self.root.iconbitmap("cek.ico")
        self.con = const() #Initialize constants
        self.heading() # Show Conway title above Canvas

        self.canvas = Canvas(self.root, width = self.con.WIDTH, height = self.con.HEIGHT,bg = self.con.CANVAS_COLOUR)
        self.grid_lines() #Draw lines in Canvas
        self.canvas.bind("<Button-1>",func=self.onObjectClick)

        self.canvas.pack()
        
        self.algo = gol(self.canvas)

        self.b1 = ttk.Button(self.root, text="Pause Button", command=self.button_func)
        self.b2 = ttk.Button(self.root, text = "Click to run animation", command = self.run, state = "disabled")
        self.b3 = ttk.Button(self.root, text = "Step", command = self.algo.automate)
        self.reset = ttk.Button(self.root, text= "Reset", command = self.reset_func)
        self.randomize = ttk.Button(self.root, text="Randomize", command = self.random_cells)

        self.status_var = StringVar(self.root)
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief= RIDGE, anchor = W)

        self.save_button = ttk.Button(self.root, text = "Save", command= self.save_pattern)
        self.open_button = ttk.Button(self.root, text="Open...", command = self.read)

        self.status_bar.pack(side=BOTTOM, fill=X)
        self.b1.pack(side = LEFT)
        self.b3.pack(side = LEFT)
        self.b2.pack(side = LEFT)

        self.randomize.pack(side = RIGHT)
        self.reset.pack(side = RIGHT)


        self.save_button.pack()
        self.open_button.pack()
        self.root.resizable(False, False)

    def heading(self):
        titleFrame = Frame(self.root)
        font = tkFont.Font(family="Script Mt Bold", size=20)
        label = ttk.Label(titleFrame, text="   Conway's\nGame of Life", font=font)
        titleFrame.pack()
        label.pack()

    def grid_lines(self):

        # Add tags to all cells to find them easily.
        for x in range(self.con.WIDTH//self.con.DIV):
            x *= self.con.DIV
            for y in range(self.con.HEIGHT // self.con.DIV):
                y *= self.con.DIV
                id = self.canvas.create_rectangle(x,y, x+self.con.DIV, y+self.con.DIV, fill = self.con.CANVAS_COLOUR)

                self.canvas.addtag_withtag("dead", tagOrId=id)


    def onObjectClick(self,event):
        '''Handling mouse click events on objects(tiny rectangles)'''
        mx, my = self.box_loc(event.x, event.y)
        #self.status_bar.config(text = f"Cell at: {mx},{my}")
        self.status_var.set(f"Cell at: {mx},{my}")

        id = event.widget.find_closest(mx, my)[0]

        if self.canvas.itemcget(id, "fill") == self.con.FILL_COLOUR: #Item already selected
            self.canvas.itemconfigure(tagOrId=id, fill=self.con.CANVAS_COLOUR)
            self.canvas.addtag_withtag("dead", id)
            self.canvas.dtag(id, "live")
            
        elif self.canvas.itemcget(id, "fill") == self.con.CANVAS_COLOUR: #Item not selected
            self.canvas.itemconfigure(id, fill = self.con.FILL_COLOUR)
            self.canvas.addtag_withtag("live", id)
            self.canvas.dtag(id, "dead")
        
        
    def box_loc(self,x,y):
        '''Returns the coordinates of the box at the location provided'''
        box_x = (x//self.con.DIV) * self.con.DIV
        box_y = (y//self.con.DIV) * self.con.DIV
        return box_x,box_y

    def button_func(self):

        if self.algo.con.run == 0:
            self.algo.con.run = 1
            self.b1.config(text="Click to Pause")
            self.b2.config(state = "normal")

            self.status_var.set("Animation enabled")

        else:
            self.algo.con.run = 0
            self.b1.config(text="Click to run animation")
            self.b2.config(state ="disabled")

            self.status_var.set("Animation paused")  # Update status bar


    def run(self):
        #print("Running")

        if self.algo.automate():
            self.status_var.set("Automatic animation running")
            self.root.after(self.con.delay_timer, self.b2.invoke)

        else:
            self.b1.invoke()
            self.status_var.set("Automation stopped. No more live cells/ valid moves")

    def random_cells(self):
        for id in self.canvas.find_all():
            x = randint(0,10)
            if x % 7 ==0 and self.canvas.type(id) == "rectangle" and not self.algo.is_live(id):
                self.algo.dead_to_live(id)

    def reset_func(self):
        alive = self.canvas.find_withtag("live")
        for id in alive:
            self.algo.live_to_dead(id)

    def read(self):
        cells_list = save.read_file(self.con.WIDTH, self.con.HEIGHT)
        if cells_list == False: self.status_var.set("Unable to load pattern")
        else:
            import re
            pattern = re.compile(r"\d+")
            found_num = pattern.findall(cells_list)
            found_num = [int(l) for l in found_num]
            print("Reading files now...")
            self.reset_func()
            
            for id in found_num:
                self.algo.dead_to_live(id)

            self.status_var.set("Pattern Loaded")

    def save_pattern(self):
        save.save(self.canvas.find_withtag("live"), self.con.WIDTH, self.con.HEIGHT)
        self.status_var.set("Save Successful")

        

if __name__ == "__main__":
    rt = Tk()
    prog = Canvas_design(rt)
    rt.mainloop()
