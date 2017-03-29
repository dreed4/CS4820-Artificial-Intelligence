'''
Created on March 29, 2017

@author: Daniel Reed, Someel Pagaria
'''
import copy
class CheckerBoard(object):
    def __init__(self, arry):
        self.board = arry
    def getblack(self):
        #move through whole 2d array and get 1's
        arry = self.board
        rows = len(self.board)
        cols = len(self.board[0])
        
        for row in range(rows):
            print(self.board[row])
    def getred(self):
        #move through whole 2d array and get 3's
        arry= self.board
    def printboard(self):
        #iterate through and print nicely
        rows = len(self.board)
        cols = len(self.board[0])
        
        for row in range(rows):
            print(self.board[row])
    def getmoves(self, piece):
        print("getting moves")
        # need to determine a standard for the "description" of a piece
        # maybe a tuple like (coords, king=true/false) ?
        
        #if king, we know we can move forward or backward
            #if space is on board
                #if there space is occupied
                    #our piece, can't move there
                    
                    #not our piece, see if we can jump (next diagonal must be empty)
                
                #if space not occupied, can move there
            
            
        #if not a king, we can only move forward
            #if space is on board
                #if there space is occupied
                    #our piece, can't move there
                    
                    #not our piece, see if we can jump (next diagonal must be empty)
                
                #if space not occupied, can move there
    def movepiece(self, piece):
        