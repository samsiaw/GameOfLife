"""@author: Samuel T. Siaw
Algorithm for Conway's Game of Life"""

from Constants import constants as const

class GameOfLife(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.con = const()

    def check_surr(self,id):
        """Finds the coordinates of all the cells surrounding the current cell"""

        x1,y1,x2,y2 = self.canvas.coords(id) #Find coordinates of current id
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        surr = []

        for s in self.canvas.find_overlapping(x1, y1, x2, y2):
            if self.canvas.type(s).lower() == "rectangle" and s!= id:
                surr.append(s) #s is the id of overlapping cells

        return surr

    def live_can_live(self, surr): #checked_dead): #live cell's fate
        """ Applies Conway's Algorithm to the current living cell """
        num_live = 0

        for id in surr:
            if self.is_live(id): num_live += 1

        if num_live in (2,3): return True
        return False

    def dead_can_live(self, surr): #Dead cell's fate
        num_live = 0
        for id in surr:
            if self.is_live(id): num_live += 1

        if num_live == 3: return True
        return False

    def automate(self):
        #print(f"Automate started: {self.con.run}")

        if self.con.run == 1:

            to_live, to_die = [], []

            all_live_ids = self.canvas.find_withtag("live")
            #print("live:", all_live_ids)
            all_dead_ids = self.canvas.find_withtag("dead")
            #print("dead:", all_dead_ids)

            for id in all_live_ids:
                if not self.live_can_live(self.check_surr(id)): to_die.append(id)
            
            for id in all_dead_ids:
                if self.dead_can_live(self.check_surr(id)): to_live.append(id)


            for id in to_live:
                self.dead_to_live(id)
            for id in to_die:
                self.live_to_dead(id)
            if to_live == to_die ==[]:
                return False
            return True

    def live_to_dead(self,id):
        self.canvas.dtag(id, "live")
        self.canvas.addtag_withtag("dead", tagOrId=id)
        self.canvas.itemconfigure(tagOrId=id, fill=self.con.CANVAS_COLOUR)
        #print("Changed to dead")

    def dead_to_live(self,id):
        self.canvas.dtag(id, "dead")
        self.canvas.addtag_withtag("live", id)
        self.canvas.itemconfigure(tagOrId=id, fill = self.con.FILL_COLOUR)
        #print("Changed to live")

    def is_live(self,id):
        if self.canvas.itemcget(tagOrId=id, option = "fill") == self.con.FILL_COLOUR:
            return True
        return False

    def intersection(self,lst1,lst2):
        return list(set(lst1) & set(lst2))