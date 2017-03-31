import tkinter
from itertools import product
import threading

class Board_wait():
    def __init__(self,width,height,cellsize,arry):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.arry = arry
        
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        #self.canvas = tkinter.Canvas(self.root,width=self.width, height=self.height)
        canvas = tkinter.Canvas(self.root,width=self.width, height=self.height)
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
class BetterBoard(threading.Thread):

    def __init__(self,width,height,cellsize,arry):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.arry = arry
        
        
        #stays in init
        self.start()
        
    def callback(self):
        self.root.quit()
    
    def draw_rectangle(self, x1, y1, x2, y2, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        #pass
    def draw_circle(self, x1, y1, x2, y2, color):
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")
    def setarry(self, arry):
        self.arry = arry
    def refresher(self):
        print("updating gui...")
        for r in range(len(self.arry)):
            for c in range(len(self.arry[0])):
                coordX1 = (c * self.cellsize)
                coordY1 = (r * self.cellsize)
                coordX2 = coordX1 + self.cellsize
                coordY2 = coordY1 + self.cellsize
                
                color = "white" if r%2 == c%2 else "black"
                self.draw_rectangle(coordX1, coordY1, coordX2, coordY2, color)
                logicBoard  = [[0,1,0,1,0,1,0,1],
                                [1,0,1,0,1,0,1,0],
                                [0,1,0,1,0,1,0,1],
                                [0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0],
                                [3,0,3,0,3,0,3,0],
                                [0,3,0,3,0,3,0,3],
                                [3,0,3,0,3,0,3,0]]
                logicBoard = self.arry
                cell = logicBoard[r][c]
                if cell != 0:
                    pawnColor = "blue" if cell <= 2  else "red"
                    self.draw_circle(coordX1, coordY1, coordX2, coordY2, pawnColor)
        self.canvas.pack()
        self.root.after(100, self.refresher())
    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        #self.canvas = tkinter.Canvas(self.root,width=self.width, height=self.height)
        canvas = tkinter.Canvas(self.root,width=self.width, height=self.height)
        canvas.pack()
        self.canvas = canvas
        
        #came from initgui()
        #==============================
        
        print("updating gui...")
        for r in range(len(self.arry)):
            for c in range(len(self.arry[0])):
                coordX1 = (c * self.cellsize)
                coordY1 = (r * self.cellsize)
                coordX2 = coordX1 + self.cellsize
                coordY2 = coordY1 + self.cellsize
                
                color = "white" if r%2 == c%2 else "black"
                self.draw_rectangle(coordX1, coordY1, coordX2, coordY2, color)
                logicBoard  = [[0,1,0,1,0,1,0,1],
                                [1,0,1,0,1,0,1,0],
                                [0,1,0,1,0,1,0,1],
                                [0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0],
                                [3,0,3,0,3,0,3,0],
                                [0,3,0,3,0,3,0,3],
                                [3,0,3,0,3,0,3,0]]
                logicBoard = self.arry
                cell = logicBoard[r][c]
                if cell != 0:
                    pawnColor = "blue" if cell <= 2  else "red"
                    self.draw_circle(coordX1, coordY1, coordX2, coordY2, pawnColor)
        self.canvas.pack()
    #temp commented out
        self.refresher()
        self.root.mainloop()
        