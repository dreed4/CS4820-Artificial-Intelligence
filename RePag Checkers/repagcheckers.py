'''
Created on March 29, 2017

@author: Daniel Reed, Someel Pagaria
'''
from checkerboard import CheckerBoard

import math
import time

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

def getminimaxscore(successor, prevscore):
    blacks = successor.getcolorpieces("black")
    reds = successor.getcolorpieces("red")
    
    currentscore = len(blacks) - len(reds)
    
    #current score - previous score
    finalscore = currentscore - prevscore
    
    return finalscore

def minplay (successor, depth, maxdepth, maxicolor, maxtime, starttime,prevscore, alpha, beta):
    if maxicolor == "black":
        mincolor = "red"
    elif maxicolor == "red":
        mincolor = "black"
    successorscore = getminimaxscore(successor, prevscore)
    
    if successor.isgoal() == True:
        return (successor, math.inf)
    
    if depth == maxdepth:
        if successorscore < beta:
            beta = successorscore
        return (successor,successorscore,beta)
    
    successors = successor.getsuccessors(mincolor)
    
    bestscore = math.inf
    if len(successors)>0:
        bestsuccessor = successors[0]
    else:
        return (successor, math.inf)
    
    for s in successors:
        t2 = time.clock()
        totaltime =  t2 - starttime
        sscore = getminimaxscore(s, successorscore)
        if totaltime >= maxtime:
            return (bestsuccessor, sscore)
        
        maxplayreturn = maxplay(s, depth+1, maxdepth, maxicolor, maxtime, starttime, sscore,alpha, beta)
        score = maxplayreturn[1]
        
        if score < beta:
            beta = score
            
        
        if score < bestscore:
            bestsuccessor = s
            bestscore = score
        
        if alpha < beta:
            break
        
    return (successor, bestscore)
        
def maxplay (successor, depth, maxdepth, maxicolor, maxtime, starttime, prevscore, alpha, beta):
    successorscore = getminimaxscore(successor, prevscore)
    
    if successor.isgoal() == True:
        return (successor, -math.inf)
    
    if depth == maxdepth:
        #if successorscore > alpha:
        #    alpha = successorscore
        return (successor,successorscore)
    
    successors = successor.getsuccessors(maxicolor)
    
    bestscore = -math.inf
    if len(successors)>0:
        bestsuccessor = successors[0]
    else:
        return (successor, -math.inf)
        
    for s in successors:
        t2 = time.clock()
        totaltime =  t2 - starttime
        #get sscore which will be pushed as the previous score when minplay called
        #s is the current successor
        #successorscore is the score of the parent successor
        sscore = getminimaxscore(s, successorscore)
        if totaltime >= maxtime:
            return (bestsuccessor, sscore)
        
        #set a
        
        
        minplayreturn = minplay(s, depth+1, maxdepth, maxicolor, maxtime, starttime, sscore, alpha, beta)
        score = minplayreturn[1]
        if score > alpha:
            alpha = score
        
        
        if score > bestscore:
            bestsuccessor = s
            bestscore = score
            
        if alpha > beta:
            break
        
    return (successor, bestscore, alpha)
    
def minimax(node, maxdepth, maxicolor, maxtime, starttime):
    
    successors = node.getsuccessors(maxicolor)
    nodescore = getminimaxscore(node, 0)
    
    if len(successors)>0:
        bestsuccessor = successors[0]
    else:
        return node
    
    bestsuccessor = successors[0]
    bestscore = -math.inf
    depth = 0
    
    alpha = -math.inf
    beta = math.inf
    
    for successor in successors:
        score = minplay(successor, depth+1, maxdepth, maxicolor, maxtime, starttime, nodescore, alpha, beta)[1]
        if score > bestscore:
            bestsuccessor = successor
            bestscore = score
    
    return bestsuccessor


    
def id(board, maxdepth, maxicolor, aitype, maxtime):
    t1 = time.clock()
    depth = 0
    boards = board
    bestboard = board
    while(depth<=maxdepth):
        t2 = time.clock()
        totalt = t2-t1
        if totalt>=maxtime:
            break
        depth += 1
        bestboard = aitype(board, depth, maxicolor, maxtime, t1)
        
    
    return bestboard
def graphsearch (rootnode, blacksearchtype, blackaitype, redsearchtype, redaitype, maxdepth,maxtime):
    #first move player
    currentplayer = "black"
    board = rootnode
    goal = False
    stillplaying = True
    #loop to iterate back and forth for each player
    while (stillplaying == True):
        #call search function for current player
        print(currentplayer, " moving..")
        if currentplayer == "black":
            maxicolor = "black"
            board = blacksearchtype(board, maxdepth, maxicolor, blackaitype,maxtime)
            currentplayer = "red"
        else:
            maxicolor = "red"
            board = redsearchtype(board, maxdepth, maxicolor, redaitype,maxtime)
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
    
    maxtime = 5
    
    blacksearchtype = id
    blackaitype = minimax
    redsearchtype = id
    redaitype = minimax
    maxdepth = 20
    graphsearch(rootnode, blacksearchtype, blackaitype, redsearchtype, redaitype, maxdepth, maxtime)
checkersgame()
    