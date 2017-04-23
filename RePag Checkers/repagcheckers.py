'''
Created on March 29, 2017

@author: Daniel Reed, Someel Pagaria
'''
from checkerboard import CheckerBoard

import math
import time
from checkergui import *
import queue
    
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

def getminimaxscore(successor, prevscore, prevboard, currentcolor):
    #lists of pieces of each color on board
    blacks = successor.getcolorpieces("black")
    reds = successor.getcolorpieces("red")
    previousblacks = prevboard.getcolorpieces("black")
    previousreds = prevboard.getcolorpieces("red")
    
    #do color v color heuristic
    if currentcolor == "black":
        colvcol = len(blacks) - len(reds)
        currentpieces = blacks
        oppcolorpieces = reds
        oppcolor = "red"
    else:
        colvcol = len(reds) - len(blacks)
        currentpieces = reds
        oppcolorpieces = blacks
        oppcolor = "black"
    #jump priority heuristic        
    if currentcolor == "black":
        prevcolvcol = len(previousblacks) - len(previousreds)
    else:
        prevcolvcol = len(previousreds) - len(previousblacks)
    
    jpriority = colvcol - prevcolvcol
    
    #board safety
    jboards = []
    for p in oppcolorpieces:
        jboards.extend(successor.getmaxdepthjumps(successor, p))
    
    dangerscores = []    
    for jboard in jboards:
        b = jboard[0]
        amnt = len(b.getcolorpieces(currentcolor))
        dangerscores.append(colvcol - amnt)
    
    biggestdscore = 0
    for dscore in dangerscores:
        if dscore > biggestdscore:
            biggestdscore = dscore
            
    totaldangerscore = biggestdscore/len(currentpieces)*100
    #max for any is going to be 100
    
    #for colvcol, max would be 12
    colvcolpercentage = colvcol/12*100
    
    jprioritypercentage = jpriority/9*100
    
    colvcolwithmult = colvcolpercentage*0.1
    jprioritywithmult = jprioritypercentage*0.9
    
    finalscore = colvcolwithmult + jprioritywithmult - totaldangerscore
    
    return finalscore
def getminimaxscore_single_old(successor, prevscore, prevboard, currentcolor):
    blacks = successor.getcolorpieces("black")
    reds = successor.getcolorpieces("red")
    
    if currentcolor == "black":
        currentscore = len(blacks) - len(reds)
    else:
        currentscore = len(reds) - len(blacks)
        
    return currentscore
    
def getminimaxscore_old(successor, prevscore, prevboard, currentcolor):
    currentblacks = successor.getcolorpieces("black")
    currentreds = successor.getcolorpieces("red")
    previousblacks = prevboard.getcolorpieces("black")
    previousreds = prevboard.getcolorpieces("red")
    
    if currentcolor == "black":
        currentscore = len(currentblacks) - len(currentreds)
        previousscore = len(previousblacks) - len(previousreds)
    else:
        currentscore = len(currentreds) - len(currentblacks)
        previousscore = len(previousreds) - len(previousblacks)
    #current score - previous score
    
    
    finalscore = currentscore - previousscore
    
    return finalscore

def minplay (successor, depth, maxdepth, maxicolor, maxtime, starttime,prevscore, alpha, beta, prevboard):
    #placeholder var
    if maxicolor == "black":
        mincolor = "red"
    elif maxicolor == "red":
        mincolor = "black"
    successorscore = getminimaxscore(successor, prevscore, prevboard, mincolor)
    
    if successor.isgoal(mincolor) == True:
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
    t2 = time.clock()
    totaltime =  t2 - starttime
    
    for s in successors:
        t2 = time.clock()
        totaltime =  t2 - starttime
        sscore = getminimaxscore(s, successorscore, successor, mincolor)
        if totaltime >= maxtime:
            return (bestsuccessor, sscore)
        psuccessor = successor
        maxplayreturn = maxplay(s, depth+1, maxdepth, maxicolor, maxtime, starttime, sscore,alpha, beta, psuccessor)
        score = maxplayreturn[1]
        
        if score < beta:
            beta = score
            
        
        if score < bestscore:
            bestsuccessor = s
            bestscore = score
        
        if alpha < beta:
            
            break
        
    return (successor, bestscore)
        
def maxplay (successor, depth, maxdepth, maxicolor, maxtime, starttime, prevscore, alpha, beta, prevboard):
    #placeholder variable
   
    successorscore = getminimaxscore(successor, prevscore, prevboard, maxicolor)
    if successor.isgoal(maxicolor) == True:
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
        sscore = getminimaxscore(s, successorscore, successor, maxicolor)
        if totaltime >= maxtime:
            return (bestsuccessor, sscore)
        
        #set a
        
        psuccessor = successor
        minplayreturn = minplay(s, depth+1, maxdepth, maxicolor, maxtime, starttime, sscore, alpha, beta, psuccessor)
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
    nodescore = getminimaxscore(node, 0, node, maxicolor)
    
    
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
        score = minplay(successor, depth+1, maxdepth, maxicolor, maxtime, starttime, nodescore, alpha, beta, node)[1]
        if score > bestscore:
            bestsuccessor = successor
            bestscore = score
    
    return bestsuccessor


    
def id(board, maxdepth, maxicolor, aitype, maxtime):
    t1 = time.clock()
    depth = 0
    bestboard = board
    while(depth<=maxdepth):
        t2 = time.clock()
        totalt = t2-t1
        if totalt>=maxtime:
            break
        depth += 1
        
        bestboard = aitype(board, depth, maxicolor, maxtime, t1)
            
    return bestboard
def graphsearch (rootnode, blacksearchtype, blackaitype, redsearchtype, redaitype, maxdepth,maxtimeblack,maxtimered,q):
    #first move player
    currentplayer = "black"
    board = rootnode
    q.put(board.board)
    goal = False
    stillplaying = True
    numturns = 0
    
    #loop to iterate back and forth for each player
    while (stillplaying == True):
        #call search function for current player
        if board.isgoal(currentplayer) == True:
            print("we found a goal")
            goal = True
            winner = board.getwinner()
            stillplaying = False
        print(currentplayer, " moving..")
        if currentplayer == "black":
            maxicolor = "black"
            board = blacksearchtype(board, maxdepth, maxicolor, blackaitype,maxtimeblack)
            currentplayer = "red"
        else:
            maxicolor = "red"
            board = redsearchtype(board, maxdepth, maxicolor, redaitype,maxtimered)
            currentplayer = "black"
        
        #update the gui queue here
        q.put(board.board)
        #=============
        print("move made: ")
        board.printboard()
        print("")
        
        numturns += 1
        
            
    return (board, winner, numturns)
    
def test ():
    newboard = geninitcheckerboard()
    print("")
    newboard.printboard()
    successors = newboard.getsuccessors("black")
    print (successors)
    for s in successors:
        print("")
        s.printboard()
    
  
    
    
def checkersgame(q, rootarry):
    #init gui stuff first
   
    #guiboard = initgui()
    
    #rootarry = [[0,1,0,1,0,1,0,1],
    #            [1,0,1,0,1,0,1,0],
    #            [0,1,0,1,0,1,0,1],
    #            [0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0],
    #            [3,0,3,0,3,0,3,0],
    #            [0,3,0,3,0,3,0,3],
    #            [3,0,3,0,3,0,3,0]]
    
    
    
    rootnode = CheckerBoard(rootarry)
    rootnode.printboard()
    print("")
    maxtimeperturnblack = 3
    maxtimeperturnred = 3
    
    blacksearchtype = id
    blackaitype = minimax
    redsearchtype = id
    redaitype = minimax
    maxdepth = 10000000
    t1 = time.clock()
    endgame = graphsearch(rootnode, blacksearchtype, blackaitype, redsearchtype, redaitype, maxdepth, maxtimeperturnblack, maxtimeperturnred, q)
    t2 = time.clock()
    
    #time the whole game took
    totaltime = t2-t1
    
    finalboard = endgame[0]
    winner = endgame[1]
    numturns = endgame[2]
    print("Game is over. The winner is ", winner, " and the final board configuration is: ")
    finalboard.printboard()
    print("Number of turns: ", numturns)
    print("Total time taken (seconds): ", totaltime)
#print("calling repagcheckers file outside")
#checkersgame(q=None)
    