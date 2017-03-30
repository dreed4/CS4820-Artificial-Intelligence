'''
Created on March 29, 2017

@author: Daniel Reed, Someel Pagaria
'''
from checkerboard import CheckerBoard

import math

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

def getminimaxscore(successor):
    blacks = successor.getcolorpieces("black")
    reds = successor.getcolorpieces("red")
    
    score = len(blacks) - len(reds)
    
    return (successor, score)

def minplay (successor, depth, maxdepth, maxicolor):
    if maxicolor == "black":
        mincolor = "red"
    elif maxicolor == "red":
        mincolor = "black"
    
    if successor.isgoal() == True:
        return (successor, -math.inf)
    
    if depth == maxdepth:
        return getminimaxscore(successor)
    
    successors = successor.getsuccessors(mincolor)
    
    bestscore = math.inf
    
    for successor in successors:
        score = maxplay(successor, depth+1, maxdepth, maxicolor)[1]
        
        if score < bestscore:
            bestsuccessor = successor
            bestscore = score
        
    return (successor, bestscore)
        
def maxplay (successor, depth, maxdepth, maxicolor):
    
    
    if successor.isgoal() == True:
        return (successor, math.inf)
    
    if depth == maxdepth:
        return getminimaxscore(successor)
    
    successors = successor.getsuccessors(maxicolor)
    
    bestscore = -math.inf
    
    for successor in successors:
        score = minplay(successor, depth+1, maxdepth, maxicolor)[1]
        
        if score > bestscore:
            bestsuccessor = successor
            bestscore = score
        
    return (successor, bestscore)
    
def minimax(node, maxdepth, maxicolor):
    successors = node.getsuccessors(maxicolor)
    bestsuccessor = successors[0]
    bestscore = -math.inf
    depth = 0
    for successor in successors:
        score = minplay(successor, depth+1, maxdepth, maxicolor)[1]
        if score > bestscore:
            bestsuccessor = successor
            bestscore = score
    
    return bestsuccessor


    
def id(board, maxdepth, maxicolor, aitype):
    depth = 0
    boards = board
    while(depth<=maxdepth):
        bestboard = aitype(board, maxdepth, maxicolor)
        depth += 1
    
    return bestboard
def graphsearch (rootnode, blacksearchtype, blackaitype, redsearchtype, redaitype, maxdepth):
    currentplayer = "black"
    board = rootnode
    goal = False
    stillplaying = True
    #loop to iterate back and forth for each player
    while (stillplaying == True):
        #call search function for current player
        print(currentplayer, " moved..")
        if currentplayer == "black":
            maxicolor = "black"
            board = blacksearchtype(board, maxdepth, maxicolor, blackaitype)
            currentplayer = "red"
        else:
            maxicolor = "red"
            board = redsearchtype(board, maxdepth, maxicolor, redaitype)
            currentplayer = "black"
        
        board.printboard()
        print("")
        if board.isgoal() == True:
            goal = True
            stillplaying = False
            
    return board
    
def test ():
    newboard = geninitcheckerboard()
    print("")
    newboard.printboard()
    successors = newboard.getsuccessors("black")
    print (successors)
    for s in successors:
        print("")
        s.printboard()
    
    
    
def checkersgame():
    rootarry = [[0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [3,0,3,0,3,0,3,0],
                [0,3,0,3,0,3,0,3],
                [3,0,3,0,3,0,3,0]]
    
    rootnode = CheckerBoard(rootarry)
    
    blacksearchtype = id
    blackaitype = minimax
    redsearchtype = id
    redaitype = minimax
    maxdepth = 3
    graphsearch(rootnode, blacksearchtype, blackaitype, redsearchtype, redaitype, maxdepth)
checkersgame()
    