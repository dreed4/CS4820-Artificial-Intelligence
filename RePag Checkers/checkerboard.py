'''
Created on March 29, 2017

@author: Daniel Reed, Someel Pagaria
'''
import copy
from copy import deepcopy
class CheckerBoard(object):
    def __init__(self, arry):
        self.board = arry
    def setdepth(self, depth):
        self.depth = depth
    
    def getdepth(self):
        return self.getdepth()
    
    def printboard(self):
        #iterate through and print nicely
        rows = len(self.board)
        cols = len(self.board[0])
        
        for row in range(rows):
            print(self.board[row])
            
    def getcolorpieces(self, color):
        arry = self.board
        rows = len(self.board)
        cols = len(self.board[0])
        pieces = []
        for row in range(rows):
            for col in range(cols):
                if color == "black":
                    if arry[row][col] == 1 or arry[row][col] == 2:
                        pieces.append([row,col])
                elif color == "red":
                    if arry[row][col] == 3 or arry[row][col] == 4:
                        pieces.append([row,col])
        
        return pieces
    
    def getsuccessors(self, color):
        #get all pieces of specified color
        colorpieces = self.getcolorpieces(color)
        #get all moves for each piece
        boards = []
        for piece in colorpieces:
            movesarry = self.getmoves(piece)
            
            #generate boards out of all moves
            for m in movesarry:
                boards.append(m)
        return boards
    
    def getalljumps(self, piece, boards=None):
        
        jumps = []
        row = piece[0]
        column = piece[1]
        #set color of current piece
        if self.board[row][column] == 1 or self.board[row][column] == 2:
            color = "black"
            oppcolor = "red"
        else:
            color = "red"
            oppcolor = "black"
        #get all potential moves
        if self.board[row][column] == 2 or self.board[row][column] == 4:
            king = True
        else:
            king = False
        potentialmoves = []
        if color == "black":
            # do forward moves
            #row+1, column-1
            potentialmoves.append([row+1, column-1])
            #row+1, column+1
            potentialmoves.append([row+1, column+1])
            
            # if king do backward moves
            if king == True:
                #row-1, column-1
                #add to potential moves
                potentialmoves.append([row-1, column-1])
                #row-1, column+1
                #add to potential moves
                potentialmoves.append([row-1, column+1])
            
        #if red
        elif color == "red":
           # do forward moves
            #row+1, column-1
            potentialmoves.append([row-1, column-1])
            #row+1, column+1
            potentialmoves.append([row-1, column+1])
            
            # if king do backward moves
            if king == True:
                #row-1, column-1
                #add to potential moves
                potentialmoves.append([row+1, column-1])
                #row-1, column+1
                #add to potential moves
                potentialmoves.append([row+1, column+1])
        #remove out of bounds problesm
        toremove = []
        for m in potentialmoves:
            r = m[0]
            c = m[1]
            rows = 7
            cols = 7
            if r > rows or r < 0:
                toremove.append(m)
            elif c > cols or c < 0:
                toremove.append(m)
        
        #remove impossible or illegal
        for rem in toremove:
            potentialmoves.remove(rem)
        
        for m in potentialmoves:
            r = m[0]
            c = m[1]
            mcolor = None
            
            #if this position is >0 we KNOW there is a piece here
            if self.board[r][c] > 0:
                if self.board[r][c] <= 2:
                    mcolor = "black"
                else:
                    mcolor = "red"
                    
            #find the move that has a piece of opposite color
            if mcolor == oppcolor:
                
                #if next space empty, do jump, make board
                finalrow = m[0] + (m[0] - piece[0])
                finalcol = m[1] + (m[1] - piece[1])
                
                finalcoord = [finalrow, finalcol]
                
                
                
                #check if jump will be in bounds
                if finalrow < 7 and finalrow > 0 and finalcol < 7 and finalcol > 0:
                    #check if jump space is empty
                    if self.board[finalrow][finalcol] == 0:
                        jumps.append(finalcoord)
                    
        #loop through all jumps, create new boards
        jumpedstates = []
        
        #for all jumps
            #move piece
            
            #get all jumps for new board
            
            #erase old board if it had a new jump
        tmpjumps = []
        for jumpcoord in jumps:
            newobj = self.movepiece(piece, jumpcoord, True)
            tmpjumps.append((newobj,jumpcoord))
            
        for jump in tmpjumps:
            newjumps = jump[0].getalljumps(jump[1])
            if len(newjumps) > 0:
                jumpedstates.extend(newjumps)
            else:
                jumpedstates.append(jump[0])
            
        
        
        return jumpedstates
    def getmoves(self, piece):
        
        # need to determine a standard for the "description" of a piece
        # maybe a tuple like (coords, king=true/false) ?
       
        coord = piece
        row = coord[0]
        column = coord[1]
        if self.board[row][column] == 1 or self.board[row][column] == 2:
            color = "black"
        elif self.board[row][column] == 3 or self.board[row][column] == 4:
            color = "red"
            
        if self.board[row][column] == 2 or self.board[row][column] == 4:
            king = True
        else:
            king = False
        
        #get all the darn jumps
        jumps = self.getalljumps(piece)
        
        potentialmoves = []
        #if black
        if color == "black":
            # do forward moves
            #row+1, column-1
            potentialmoves.append([row+1, column-1])
            #row+1, column+1
            potentialmoves.append([row+1, column+1])
            
            # if king do backward moves
            if king == True:
                #row-1, column-1
                #add to potential moves
                potentialmoves.append([row-1, column-1])
                #row-1, column+1
                #add to potential moves
                potentialmoves.append([row-1, column+1])
            
        #if red
        elif color == "red":
           # do forward moves
            #row+1, column-1
            potentialmoves.append([row-1, column-1])
            #row+1, column+1
            potentialmoves.append([row-1, column+1])
            
            # if king do backward moves
            if king == True:
                #row-1, column-1
                #add to potential moves
                potentialmoves.append([row+1, column-1])
                #row-1, column+1
                #add to potential moves
                potentialmoves.append([row+1, column+1])
        
        
        #Throw out moves off of board
        #loop through potential moves
        
        toremove = []
        
        for m in potentialmoves:
            r = m[0]
            c = m[1]
            #if column > 7 or < 0, throw out
            if c > 7 or c < 0:
                #potentialmoves.remove(m)
                toremove.append(m)
            #if row > 7 or < 0, throw out
            elif r > 7 or r < 0:
                #potentialmoves.remove(m)
                toremove.append(m)
            #Throw out moves of spaces occupied by same color
            elif self.board[r][c] > 0:
                toremove.append(m)
        
        #remove all illegal        
        for rem in toremove:
            potentialmoves.remove(rem)
            
        #return new boards with piece moved where it can move
        moveboards = []
        for p in potentialmoves:
            board = self.movepiece(piece, p, False)
            moveboards.append(board)
        #returns True with jumps, False with regular moves
        if len(jumps) > 0:
            return (jumps)
        else:
            return (moveboards)
    def movepiece(self, piece, newcoord, jump):
        piecerow=piece[0]
        piececol=piece[1]
        if self.board[piecerow][piececol] == 1 or self.board[piecerow][piececol] == 2:
            color = "black"
        elif self.board[piecerow][piececol] == 3 or self.board[piecerow][piececol] == 4:
            color = "red"
            
        newrow=newcoord[0]
        newcol=newcoord[1]
        
        newboard = copy.deepcopy(self.board)
        oldboard = copy.deepcopy(self.board)
        if jump == True:
            newboard[piecerow][piececol] = 0
            newboard[newrow][newcol] = oldboard[piecerow][piececol]
            
            #remove jumped piece
            #first get coord of jumped piece
            jpiecerow = int((newrow - piecerow)/2 + piecerow) 
            jpiececol = int((newcol - piececol)/2 + piececol)
            newboard[jpiecerow][jpiececol] = 0
        else:
            #turn to king or not????????
            if color == "red":
                if newrow == 0:
                    #then we wuz kangz
                    newboard[newrow][newcol] = 4
                else:
                    #we wuznt kangz
                    newboard[newrow][newcol] = oldboard[piecerow][piececol]
            elif color == "black":
                if newrow == 7:
                    #then we wuz kangz
                    newboard[newrow][newcol] = 2
                else:
                    #we wuznt kangz
                    newboard[newrow][newcol] = oldboard[piecerow][piececol]
                    
            newboard[piecerow][piececol] = 0
            
        
        newboardobj = CheckerBoard(newboard)
        return newboardobj
    def getwinner(self):
        blacks = getcolorpieces("black")
        reds = getcolorpieces("red")
        if self.isgoal() == True:
            if len(blacks) > 0:
                return ("black")
            else:
                return ("red")
    def isgoal(self):
        #find out if this board is a goal
        #if either color is not on board, it is a goal with opposite color as winner
        blacks = self.getcolorpieces("black")
        reds = self.getcolorpieces("red")
        
        if len(blacks) == 0:
            return True
        elif len(reds) == 0:
            return True
        else:
            return False