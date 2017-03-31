import tkinter as tk
from itertools import product
import threading
import queue
import time
import repagcheckers

class Board_wait():
    def __init__(self,width,height,cellsize,arry):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.arry = arry
        
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        #self.canvas = tkinter.Canvas(self.root,width=self.width, height=self.height)
        canvas = tk.Canvas(self.root,width=self.width, height=self.height)
        canvas.pack()
        self.canvas = canvas
        
        self.root.after(100,self.redraw())
        
        #self.root.mainloop()
    def draw_rectangle(self, x1, y1, x2, y2, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        #pass
    def draw_circle(self, x1, y1, x2, y2, color):
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")
    def setarry(self, arry):
        self.arry = arry
    def callback(self):
        self.root.quit()
    def redraw(self):
        #spawn thread 
        
        
        print("updating gui...")
        for r in range(len(self.arry)):
            for c in range(len(self.arry[0])):
                coordX1 = (c * self.cellsize)
                coordY1 = (r * self.cellsize)
                coordX2 = coordX1 + self.cellsize
                coordY2 = coordY1 + self.cellsize
                
                color = "white" if r%2 == c%2 else "black"
                self.draw_rectangle(coordX1, coordY1, coordX2, coordY2, color)
                
                logicBoard = self.arry
                cell = logicBoard[r][c]
                if cell != 0:
                    pawnColor = "blue" if cell <= 2  else "red"
                    self.draw_circle(coordX1, coordY1, coordX2, coordY2, pawnColor)
        self.canvas.pack()
        self.root.update()
        self.root.update_idletasks()
        #self.root.after(0,self.redraw())
        
#==================================        
class Gui:
    def __init__(self,root, width,height,cellsize,arry, q):
        #threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.cellsize = cellsize
        
        self.drawnonce = 0
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        
        self.q = q
        if self.q.empty() == False:
            self.arry = self.q.get(0)
        #self.canvas = tkinter.Canvas(self.root,width=self.width, height=self.height)
        canvas = tk.Canvas(self.root,width=self.width, height=self.height)
        canvas.pack()
        self.canvas = canvas
        #self.root.after(100,self.eachloop())
        self.initdraw()
        self.redraw()
        #self.root.mainloop()
    def draw_rectangle(self, x1, y1, x2, y2, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        #pass
    def draw_circle(self, x1, y1, x2, y2, color):
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")
        
    def draw_king(self, x1, y1, x2, y2, color):
        self.canvas.create_text(text="KING")
    def setarry(self, arry):
        self.arry = arry
    def callback(self):
        self.root.quit()
    
    def initdraw(self):
        print("called initdraw")
        
        
        for r in range(len(self.arry)):
            for c in range(len(self.arry[0])):
                coordX1 = (c * self.cellsize)
                coordY1 = (r * self.cellsize)
                coordX2 = coordX1 + self.cellsize
                coordY2 = coordY1 + self.cellsize
                
                color = "white" if r%2 == c%2 else "black"
                self.draw_rectangle(coordX1, coordY1, coordX2, coordY2, color)
                
                logicBoard = self.arry
                    
                cell = logicBoard[r][c]
                kingme = False
                if cell != 0:
                    if cell <= 2:
                        pawnColor = "blue"
                        if cell == 2:
                            #then it's a king
                            kingme = True
                    else:
                        pawnColor = "red"
                        if cell == 4:
                            #then it's a king
                            kingme = True
                    self.draw_circle(coordX1, coordY1, coordX2, coordY2, pawnColor)
                    if kingme == True:
                        
                    self.canvas.pack()
                    
        self.root.update()
        self.root.update_idletasks()
    def redraw(self):
        
        if self.q.empty() == False:
            self.arry = self.q.get(0)
            #print("found something in queue")
        
        
        #print ("updating gui...")
        for r in range(len(self.arry)):
            for c in range(len(self.arry[0])):
                coordX1 = (c * self.cellsize)
                coordY1 = (r * self.cellsize)
                coordX2 = coordX1 + self.cellsize
                coordY2 = coordY1 + self.cellsize
                
                color = "white" if r%2 == c%2 else "black"
                self.draw_rectangle(coordX1, coordY1, coordX2, coordY2, color)
                
                logicBoard = self.arry
                    
                cell = logicBoard[r][c]
                if cell != 0:
                    pawnColor = "blue" if cell <= 2  else "red"
                    self.draw_circle(coordX1, coordY1, coordX2, coordY2, pawnColor)
                    self.canvas.pack()
       
        
        if self.q.empty() == False:
            self.root.update()
            self.root.update_idletasks()
        self.root.after(50,self.redraw())
        
class Threader(threading.Thread):

    def __init__(self, q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.q = q
        self.start()
        
    def run(self):
        repagcheckers.checkersgame(self.q)
        
if __name__ == "__main__":
    width = 400
    height = 400
    cellsize = 40
    arry = [[0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [3,0,3,0,3,0,3,0],
            [0,3,0,3,0,3,0,3],
            [3,0,3,0,3,0,3,0]]
    
    
    root = tk.Tk()
    root.title("RePag Checkers")
    q = queue.Queue()
    
    Threader(q)
    
    my_gui = Gui(root, width, height, cellsize, arry, q)
    
    root.mainloop()
    
    