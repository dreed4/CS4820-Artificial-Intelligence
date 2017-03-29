'''
Created on March 29, 2017

@author: Daniel Reed, Someel Pagaria
'''
from checkerboard import CheckerBoard

# Generate new board
# 0: empty
# 1: black
# 2: black king
# 3: red
# 4: red king
def geninitcheckerboard ():
    #create array
    
    arry = [[0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [3,0,3,0,3,0,3,0],
            [0,3,0,3,0,3,0,3],
            [3,0,3,0,3,0,3,0]]
    
    newboard = CheckerBoard(arry)
    newboard.printboard()
    
    return newboard
def main ():
    newboard = geninitcheckerboard()
    
main()
    