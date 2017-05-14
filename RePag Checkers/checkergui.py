import tkinter as tk
import threading
import queue
import repagcheckers
class Gui_Move(object):
    def __init__(self):
        self.x1 = -1
        self.y1 = -1
        self.r1 = -1
        self.c1 = -1
        
        self.x2 = -1
        self.y2 = -1
        self.r2 = -1
        self.c2 = -1
    def resetmove(self):
        print("resetmove called")
        self.x1 = -1
        self.y1 = -1
        self.r1 = -1
        self.c1 = -1
        
        self.x2 = -1
        self.y2 = -1
        self.r2 = -1
        self.c2 = -1
        
    def set(self, x, y):
        if self.x1 == -1:
            self.x1 = x
            self.y1 = y
            self.r1 = int(y/40) + 1
            self.c1 = int(x/40) + 1
        elif self.x2 == -1:
            self.x2 = x
            self.y2 = y
            self.r2 = int(y/40) + 1
            self.c2 = int(x/40) + 1
        else:
            
            self.resetmove()
class Gui:
    def __init__(self,root, width,height,cellsize,arry, q):
        #threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.arry = arry
        self.drawnonce = 0
        self.guimove = Gui_Move()
        
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
       
        
        self.q = q
        if self.q.empty() == False:
            self.arry = self.q.get(0)
        #self.canvas = tkinter.Canvas(self.root,width=self.width, height=self.height)
        canvas = tk.Canvas(self.root,width=self.width, height=self.height)
        canvas.bind("<Button-1>", self.clickcallback)
        b = tk.Button(self.root, text="Do Move", command=self.domovecallback)
        b.pack()
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
        
    def clickcallback(self, event):
        x = event.x
        y = event.y
        self.guimove.set(x, y)
        print("GuiMove square 1: ", self.guimove.r1, self.guimove.c1)
        print("GuiMove square 2: ", self.guimove.r2, self.guimove.c2)
        print()
    def domovecallback(self):
        
        print("Do move clicked!")
        self.guimove.resetmove()
    def initdraw(self):
        
        
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
                    kingme = False
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
                        #sort gui out for kinging things
                        
                        pass
                    self.canvas.pack()
                    
        self.root.update()
        self.root.update_idletasks()
    def redraw(self):
        redrawit = False
        if self.q.empty() == False:
            self.arry = self.q.get(0)
            redrawit = True
        
        #print ("updating gui...")
        if redrawit == True:
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
                        kingme = False
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
                            #sort gui out for kinging things
                            #we need the circle to be a bit smaller than the first
                            #if we want 50% of the size we'll do 
                            #quarterX = (x2 - x1)/4, then x1 = x1 + quarterX, x2 = x2 - quarterX
                            quarterX = (coordX2 - coordX2)/4
                            coordX1 = coordX1 + quarterX
                            coordX2 = coordX2 - quarterX
                            
                            quarterY = (coordY2 - coordY1)/4
                            coordY1 = coordY1 + quarterY
                            coordY2 = coordY2 - quarterY
                            self.draw_circle(coordX1, coordY1, coordX2, coordY2, pawnColor)
                        self.canvas.pack()
        
        if self.q.empty() == False:
            self.root.update()
            self.root.update_idletasks()
        
        #this is a lambda function in an attempt to fix the infinite recursion issue
        #not sure why using a lambda is supposed to fix this, but the stackoverflow
        #says it should 
        self.root.after(50, lambda: self.redraw())
        
class Threader(threading.Thread):

    def __init__(self, q, rootarry, pmvq, checkmvq):
        threading.Thread.__init__(self)
        self.daemon = True
        self.q = q
        self.pmvq = pmvq
        self.checkmvq = checkmvq
        
        self.start()
        self.rootarry = rootarry
    def run(self):
        repagcheckers.checkersgame(self.q, rootarry, pmvq, checkmvq)
        
if __name__ == "__main__":
    width = 400
    height = 400
    cellsize = 40
    rootarry = [[0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [3,0,3,0,3,0,3,0],
            [0,3,0,3,0,3,0,3],
            [3,0,3,0,3,0,3,0]]
    
    teetarry = [[0,0,0,0,0,0,0,0],
                [0,0,1,0,1,0,0,0],
                [0,0,0,3,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,3,0,0,0,3,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,3,0,3,0,0],
                [0,0,0,0,0,0,0,0]]
    
    root = tk.Tk()
    root.title("RePag Checkers")
    q = queue.Queue()
    
    #playermove queue
    pmvq = queue.Queue
    #check playermove queue
    checkmvq = queue.Queue
    
    Threader(q, rootarry, pmvq, checkmvq)
    
    my_gui = Gui(root, width, height, cellsize, rootarry, q)
    
    root.mainloop()
    
    