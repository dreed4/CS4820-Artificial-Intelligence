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

    newboard = CheckerBoard(arry)
    
    return newboard

def getminimaxscore(successor, prevscore, prevboard, currentcolor):
    blacks = successor.getcolorpieceswithkings("black")
    reds = successor.getcolorpieceswithkings("red")
    
    if currentcolor == "black":
        currentpieces = blacks[0]
        currentpieces.extend(blacks[1])
        oppcolorpieces = reds[0]
        oppcolorpieces.extend(reds[1])
        oppcolor = "red"
        
    else:
        
        currentpieces = reds[0]
        currentpieces.extend(reds[1])
        oppcolorpieces = blacks[0]
        oppcolorpieces.extend(blacks[1])
        oppcolor = "black"
        
    #flags
    red_docolvcol = True
    red_dodangerscore = True
    red_dojumpscore = True
    red_dopositionalscore = True
    
    black_docolvcol = True
    black_dodangerscore = True
    black_dojumpscore = True
    black_dopositionalscore = True
    
    #init scores to 0
    colvcolscore = 0
    dangerscore = 0
    jumpscore = 0
    positionalscore = 0
    
    #get piece multiplier
    pieceslost = 12 - len(currentpieces)
    enemieslost = 12 - len(oppcolorpieces)
    piecemultiplier = 1.2**pieceslost
    enemypiecemultiplier = 1.2**enemieslost
    
    if currentcolor == "red":
        if red_docolvcol == True:
            colvcolscore = getcolvcolscore(blacks, reds, currentcolor, piecemultiplier, enemypiecemultiplier)
        if red_dodangerscore == True:
            dangerscore = getdangerscore(successor, currentcolor, currentpieces, oppcolorpieces)
        if red_dojumpscore == True:
            jumpscore = getjumpscore(successor, currentpieces, oppcolorpieces, oppcolor)
        if red_dopositionalscore == True:
            positionalscore = getpositionalscore(currentpieces, oppcolorpieces)
        
    elif currentcolor == "black":
        if black_docolvcol == True:
            colvcolscore = getcolvcolscore(blacks, reds, currentcolor, piecemultiplier, enemypiecemultiplier)
        if black_dodangerscore == True:
            dangerscore = getdangerscore(successor, currentcolor, currentpieces, oppcolorpieces)
        if black_dojumpscore == True:
            jumpscore = getjumpscore(successor, currentpieces, oppcolorpieces, oppcolor)
        if black_dopositionalscore == True:
            positionalscore = getpositionalscore(currentpieces, oppcolorpieces)
    
    #do weighting
    colvcolweighted = colvcolscore * 5
    dangerscoreweighted = -dangerscore
    jumpscoreweighted = jumpscore
    positionalscoreweighted = positionalscore
    
    totalscore = colvcolweighted + dangerscoreweighted + jumpscoreweighted + positionalscoreweighted
    
    return totalscore
    
def getcolvcolscore (blacks, reds, currentcolor, piecemultiplier, enemypiecemultiplier):
    if currentcolor == "black":
        colvcol = ((len(blacks[0]) + (len(blacks[1])*1.5))*piecemultiplier) - ((len(reds[0]) + (len(reds[1])*1.5))*enemypiecemultiplier)
    else:
        colvcol = ((len(reds[0]) + (len(reds[1])*1.5))*piecemultiplier) - ((len(blacks[0]) + (len(blacks[1])*1.5))*enemypiecemultiplier)
        
    colvcolpercentage = colvcol/18*100
    
    return colvcolpercentage

def getdangerscore (successor, currentcolor, currentpieces, oppcolorpieces):
    jboards = []
    for p in oppcolorpieces:
        jboards.extend(successor.getmaxdepthjumps(successor, p))
    
    dangerscores = []    
    for jboard in jboards:
        b = jboard[0]
        amnt = len(b.getcolorpieces(currentcolor))
        dangerscores.append((len(currentpieces)-len(oppcolorpieces)) - amnt)
    
    biggestdscore = 0
    for dscore in dangerscores:
        if dscore > biggestdscore:
            biggestdscore = dscore
    if (len(currentpieces)>0):        
        totaldangerscore = biggestdscore/len(currentpieces)*100
    else: 
        totaldangerscore = 0
        
    return totaldangerscore

def getjumpscore(successor, currentpieces, oppcolorpieces, oppcolor):
    jboards = []
    for p in currentpieces:
        jboards.extend(successor.getmaxdepthjumps(successor, p))
        
    jumpscores = []
    for jboard in jboards:
        b = jboard[0]
        amnt = len(b.getcolorpieces(oppcolor))
        jumpscores.append(len(oppcolorpieces) - amnt)
        
    biggestjscore = 0
    for jscore in jumpscores:
        if jscore > biggestjscore:
            biggestjscore = jscore
    if (len(oppcolorpieces)):
        totaljumpscore = biggestjscore/len(oppcolorpieces)*100
    else:
        totaljumpscore = 0
    
    return totaljumpscore

def getpositionalscore(currentpieces, oppcolorpieces):
    posscore = 0
    if ((len(currentpieces) + len(oppcolorpieces)) > 8):
        scores = [[1,1,1,1,1,1,1,1],
                 [1,2,2,2,2,2,2,1],
                 [1,2,3,3,3,3,2,1],
                 [1,2,3,4,4,3,2,1],
                 [1,2,3,4,4,3,2,1],
                 [1,2,3,3,3,3,2,1],
                 [1,2,2,2,2,2,2,1],
                 [1,1,1,1,1,1,1,1]]
    else:
        scores = [[1,1,1,1,1,1,1,1],
                 [1,3,3,3,3,3,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,3,3,3,3,3,1],
                 [1,1,1,1,1,1,1,1]]
    for p in currentpieces:
        r = p[0]
        c = p[1]
        posscore = posscore + scores[r][c]
        
    posscore = posscore/32*100
    
    return posscore

def getminimaxscore_old(successor, prevscore, prevboard, currentcolor):
    #lists of pieces of each color on board
    blacks = successor.getcolorpieceswithkings("black")
    reds = successor.getcolorpieceswithkings("red")
      
    
    if currentcolor == "black":
        currentpieces = blacks[0]
        currentpieces.extend(blacks[1])
        oppcolorpieces = reds[0]
        oppcolorpieces.extend(reds[1])
        oppcolor = "red"
        pieceslost = 12 - len(currentpieces)
        enemieslost = 12 - len(oppcolorpieces)
        piecemultiplier = 1.2**pieceslost
        enemypiecemulitplier = 1.2**enemieslost
        colvcol = ((len(blacks[0]) + (len(blacks[1])*1.5))*piecemultiplier) - ((len(reds[0]) + (len(reds[1])*1.5))*enemypiecemulitplier)
    else:
        
        currentpieces = reds[0]
        currentpieces.extend(reds[1])
        oppcolorpieces = blacks[0]
        oppcolorpieces.extend(blacks[1])
        oppcolor = "black"
        pieceslost = 12 - len(currentpieces)
        enemieslost = 12 - len(oppcolorpieces)
        piecemultiplier = 1.2**pieceslost
        enemypiecemulitplier = 1.2**enemieslost
        colvcol = ((len(reds[0]) + (len(reds[1])*1.5))*piecemultiplier) - ((len(blacks[0]) + (len(blacks[1])*1.5))*enemypiecemulitplier)
   
    
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
    if (len(currentpieces)>0):        
        totaldangerscore = biggestdscore/len(currentpieces)*100
    else: 
        totaldangerscore = 0
    
    #jump scores
    jboards = []
    for p in currentpieces:
        jboards.extend(successor.getmaxdepthjumps(successor, p))
        
    jumpscores = []
    for jboard in jboards:
        b = jboard[0]
        amnt = len(b.getcolorpieces(oppcolor))
        jumpscores.append(len(successor.getcolorpieces(oppcolor)) - amnt)
        
    biggestjscore = 0
    for jscore in jumpscores:
        if jscore > biggestjscore:
            biggestjscore = jscore
    if (len(oppcolorpieces)):
        totaljumpscore = biggestjscore/len(oppcolorpieces)*100
    else:
        totaljumpscore = 0

    #position scoring
    #posmax : 32
    posscore = 0
    if ((len(currentpieces) + len(oppcolorpieces)) > 8):
        scores = [[1,1,1,1,1,1,1,1],
                 [1,2,2,2,2,2,2,1],
                 [1,2,3,3,3,3,2,1],
                 [1,2,3,4,4,3,2,1],
                 [1,2,3,4,4,3,2,1],
                 [1,2,3,3,3,3,2,1],
                 [1,2,2,2,2,2,2,1],
                 [1,1,1,1,1,1,1,1]]
    else:
        scores = [[1,1,1,1,1,1,1,1],
                 [1,3,3,3,3,3,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,5,5,5,5,3,1],
                 [1,3,3,3,3,3,3,1],
                 [1,1,1,1,1,1,1,1]]
    for p in currentpieces:
        r = p[0]
        c = p[1]
        posscore = posscore + scores[r][c]
        
    posscore = posscore/32*100
    
    #for colvcol, max would be 18
    colvcolpercentage = colvcol/18*100
    
    colvcolwithmult = colvcolpercentage*5
    
    dangerscorewithmult = totaldangerscore
    
    jumpscorewithmult = totaljumpscore
    if len(currentpieces) > 0:
        posscorewithmult = posscore*(1/len(currentpieces))
    else:
        posscorewithmult = posscore*0
        
    #max finalscore = 10
    finalscore = colvcolwithmult + (-dangerscorewithmult) + posscorewithmult + jumpscorewithmult
    if len(currentpieces) <= 0:
        finalscore = -math.inf
    return finalscore
def getminimaxscore_single_old(successor, prevscore, prevboard, currentcolor):
    blacks = successor.getcolorpieces("black")
    reds = successor.getcolorpieces("red")
    
    if currentcolor == "black":
        currentscore = len(blacks) - len(reds)
    else:
        currentscore = len(reds) - len(blacks)
        
    return currentscore

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
        t1 = time.clock()
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
        t2 = time.clock()
        #update the gui queue here
        q.put(board.board)
        #=============
        print("move made: ")
        board.printboard()
        print("")
        print("Time taken for move: ", (t2-t1))
        numturns += 1
        print("Turn Number: ", numturns)
            
    return (board, winner, numturns)
    
def humanplay(node, maxdepth, maxicolor, maxtime, starttime):
    #get which piece to move
    
    #move piece gen player board
    
    #get all successor of previous board
    
    #check to see that player is in list of successors
    
    #as long as it is in the list of successors, we can return playerboard
    
    
    pass
    #return playerboard

def checkersgame(q, rootarry, pmvq, checkmvq):
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
    maxtimeperturnblack = 8
    maxtimeperturnred = 8
    
    blacksearchtype = id
    blackaitype = minimax
    redsearchtype = id
    redaitype = minimax
    maxdepth = 5
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
    
#old calls
#print("calling repagcheckers file outside")
#checkersgame(q=None)
    