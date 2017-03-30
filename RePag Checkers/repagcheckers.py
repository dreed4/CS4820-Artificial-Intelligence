'''
Created on March 29, 2017

@author: Daniel Reed, Someel Pagaria
'''
from checkerboard import CheckerBoard


    
def evalutatesuccessors (evalfn):
    print()
    
    
    
    
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
    
    arry = [[0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [0,0,3,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [3,0,3,0,3,0,3,0],
            [0,3,0,3,0,3,0,3],
            [3,0,3,0,3,0,3,0]]
    
    arry = [[2,0,0,0,0,0,0,0],
            [0,3,0,3,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,3,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,3,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]
    
    newboard = CheckerBoard(arry)
    
    return newboard

def graphsearch (rootnode, blacksearchtype, redsearchtype):
    #loop to itarate back and forth for each player
    # red black red black etc
    #check if goal
    
    #each iteration, call getsuccessors
    
    #each iteration, evaluate successors
    
    #make move
    print()
    
def main ():
    newboard = geninitcheckerboard()
    print("")
    newboard.printboard()
    successors = newboard.getsuccessors("black")
    print (successors)
    for s in successors:
        print("")
        s.printboard()
    
    
    
    
main()
    