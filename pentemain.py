from pprint import pprint
import matplotlib.pyplot as plt
from itertools import permutations
import time

import math
import copy
import itertools
import numpy as np
whiteCapture, blackCapture = 0, 0
row_name = ['19','18','17','16','15','14','13','12','11','10','9','8','7','6','5','4','3','2','1']
col_name = ['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T']

blackPlayer = -1
whitePlayer = 1

blackWins = -math.inf
whiteWins = math.inf

# blackWins = -5
# whiteWins = 5
draw = 0.1

ALPHA, BETA = -math.inf, math.inf
MAXDEPTH = 3

class penteBoard:
    def __init__(self, board, whiteCapture=0, blackCapture=0):
        self.board = copy.deepcopy(board)
        self.whiteCapture = whiteCapture #number of pieces captured by white
        self.blackCapture = blackCapture #number of pieces captured by black
        self.blankSpots = {}
        self.whitePieces = {}
        self.blackPieces = {}
        self.initializePieces()
      
    def checkFinalCaptureState(self, playerColor):
        if playerColor==-1 and self.blackCapture==5: #black piece move
            return True

        if playerColor==1 and self.whiteCapture==5: #white piece move
            return True
    
        return False
    
    
    def initializePieces(self):
        for i in range(19):
            for j in range(19):
                if self.board[i][j] in [".", 0]:
                    self.blankSpots[(i,j)] = [i,j]
                    self.board[i][j] = 0

                elif self.board[i][j] in ['b', -1]:
                    self.board[i][j] = -1
                    self.blackPieces[(i,j)] = [i,j]
                
                elif self.board[i][j] in ['w', 1]:
                    self.board[i][j] = 1
                    self.whitePieces[(i,j)] = [i,j]
        # print(self.board,"---")
        
    def sortingTheBlankSpots(self, BlankSpots, player):

        patterns = {}
        mappingInt2Char={0:".", -1:"b", 1:"w"}
        for eachp in set(["".join(x) for x in list(permutations('wwww.'))]):
            patterns[eachp] = math.inf if player == whitePlayer else math.pow(10, 10)

        for eachp in set(["".join(x) for x in list(permutations('bbbb.'))]):
            patterns[eachp] = math.inf if player == blackPlayer else math.pow(10, 10)
            
        for eachp in set(["".join(x) for x in list(permutations('www..'))]):
            patterns[eachp] = math.pow(10, 6) if player == whitePlayer else math.pow(10, 5)
            # if eachp not in ['www..', '..www', '.www.']:
            #     patterns[eachp] = math.pow(10, 6) if player == blackPlayer else math.pow(10, 5)

         
        for eachp in set(["".join(x) for x in list(permutations('bbb..'))]):
            patterns[eachp] = math.pow(10, 6) if player == blackPlayer else math.pow(10,5)
            # if eachp not in ['bbb..', '..bbb', '.bbb.']:
            #     patterns[eachp] = math.pow(10, 6) if player == whitePlayer else math.pow(10, 5)

        for eachp in set(["".join(x) for x in list(permutations('ww..'))]):
            patterns[eachp] = math.pow(10, 5) if player == whitePlayer else math.pow(10, 3)
        
        for eachp in set(["".join(x) for x in list(permutations('bb..'))]):
            patterns[eachp] = math.pow(10, 5) if player == blackPlayer else math.pow(10,3)
        
        for eachp in set([".wwbb","bww.b","bbww.", "b.wwb"]): #black capturing 
            patterns[eachp] = math.inf if self.blackCapture==4 else math.pow(10, 5)
        
        for eachp in set([".wwbw","bww.w","wbww.", "w.wwb"]): #black capturing 
            patterns[eachp] = math.inf if self.blackCapture==4 else math.pow(10, 5)
        
        for eachp in set([".wwb.","bww..",".bww.", ".wbb."]): #black capturing 
            patterns[eachp] = math.inf if self.blackCapture==4 else math.pow(10, 4.5)
        
        for eachp in set([".bbww","wbb.w","wwbb.", "w.bbw"]): #white capturing 
            patterns[eachp] = math.inf if self.whiteCapture==4 else math.pow(10, 5)
        
        for eachp in set([".bbwb","wbb.b","bwbb.", "w.bbw"]): #white capturing 
            patterns[eachp] = math.inf if self.whiteCapture==4 else math.pow(10, 5)
        
        for eachp in set([".bbw.","wbb..",".wbb.", ".bbw."]): #white capturing
            patterns[eachp] = math.inf if self.whiteCapture==4 else math.pow(10, 4.5)
        
        for eachp in set(["".join(x) for x in list(permutations('wb...'))]):
            patterns[eachp] = math.pow(10,1)
        

        emptyCellScore = {}
        for possibleCellsKey, _ in BlankSpots.items():
            score = 0 
            i,j = possibleCellsKey[0], possibleCellsKey[1]

            neighbours = {(i-4,j-4):[[i-4,j-4],[i-3,j-3],[i-2,j-2],[i-1,j-1], [i,j]],
                    (i-4,j):[[i-4,j],[i-3,j],[i-2,j],[i-1,j], [i,j]], 
                    (i-4,j+4):[[i-4,j+4],[i-3, j+3], [i-2,j+2], [i-1,j+1],[i,j]], 
                    (i,j-4):[[i,j-4], [i,j-3], [i,j-2],[i,j-1], [i,j]], 
                    (i,j+4):[[i,j],[i,j+1], [i,j+2],[i,j+3], [i,j+4]], 
                    (i+4,j-4):[[i,j], [i+1, j-1], [i+2,j-2],[i+3,j-3], [i+4, j-4]], 
                    (i+4,j):[[i,j],[i+1,j], [i+2,j],[i+3,j], [i+4, j]], 
                    (i+4,j+4):[[i,j],[i+1,j+1], [i+2,j+2],[i+3,j+3], [i+4, j+4]],
                    }
            
            startendneighbours = {
                (i,j-4):(i,j+4),
                (i-4,j):(i+4,j),
                (i-4, j+4): (i+4, j-4),
                (i-4,j-4):(i+4, j+4)
            }

            
            for start,end in startendneighbours.items():
                si = start[0]
                sj = start[1]
                ei = end[0]
                ej = end[1]

                listof9patterns = ''
                if start==(i,j-4) and end==(i,j+4):
                    for k in range(sj, ej+1):
                        if 0 <= si < len(self.board) and 0 <= k < len(self.board[0]):
                            listof9patterns+=mappingInt2Char[self.board[si][k]]
                    # print("pattern 9----",listof9patterns, len(listof9patterns), )

                elif start==(i-4,j) and end==(i+4,j):
                    for k in range(si, ei+1):
                        if 0 <= k < len(self.board) and 0 <= sj < len(self.board[0]):
                            listof9patterns+=mappingInt2Char[self.board[k][sj]]
                    # print("pattern 9----",listof9patterns, len(listof9patterns))
                
                elif start==(i-4,j+4) and end==(i+4,j-4):
                    for t in range(9):
                        ki = si + t
                        kj = sj - t

                        if 0 <= ki < len(self.board) and 0 <= kj < len(self.board[0]):
                            listof9patterns+=mappingInt2Char[self.board[ki][kj]]
                    # print("pattern 9----",listof9patterns, len(listof9patterns))
                
                elif start==(i-4,j-4) and end==(i+4,j+4):
                    for t in range(9):
                        ki = si + t
                        kj = sj + t

                        if 0 <= ki < len(self.board) and 0 <= kj < len(self.board[0]):
                            listof9patterns+=mappingInt2Char[self.board[ki][kj]]
                
                    # print("pattern 9----",listof9patterns, len(listof9patterns))

            
                window_size = 5
                window=''
                for ind in range(len(listof9patterns) - window_size + 1):
                    window = listof9patterns[ind:ind+window_size]
                    # print("window", window)

                    if window in patterns.keys():
                        score+=patterns[window]
                        # print("score",patterns[window], score)

            emptyCellScore[possibleCellsKey] = score


                        
            # for key, value in neighbours.items():
            #     ni, nj = key[0], key[1]
            #     if 0 <= ni < len(self.board) and 0 <= nj < len(self.board[0]):
            #         # print("i=",i," ni=", ni, "j=", j, "nj=", nj)
            #         p=""
            #         for cell in value:
            #             p+=mappingInt2Char[self.board[cell[0]][cell[1]]]
            #         if p in patterns.keys():
            #             score+=patterns[p]
                    
            # emptyCellScore[possibleCellsKey] = score
        # print("Before sorting, emptyCellScore= ",emptyCellScore, "\n")
    
        sortedlistofemptycell = sorted(emptyCellScore, key= lambda x : -emptyCellScore[x])
        print("After sorting, emptyCellScore= ", [(i, emptyCellScore[i]) for i in sortedlistofemptycell][0:10])
        return sortedlistofemptycell
            
        
    def getBlankSpotsWithinBoundary(self, player):
        marginBuffer=1
        minX, minY, maxX, maxY = math.inf, math.inf, (-1)*math.inf, (-1)*math.inf

        for key, _ in self.whitePieces.items():
            x,y = key[0], key[1]

            if x<minX:
                minX = x
            if y<minY:
                minY = y
            if x>maxX:
                maxX = x
            if y>maxY:
                maxY = y
        
        for key, _ in self.blackPieces.items():
            x,y = key[0], key[1]

            if x<minX:
                minX = x
            if y<minY:
                minY = y
            if x>maxX:
                maxX = x
            if y>maxY:
                maxY = y
        minX = max(minX-marginBuffer, 0)
        minY = max(minY-marginBuffer,0)
        maxX = min(maxX+marginBuffer, 18)
        maxY = min(maxY+marginBuffer, 18)

        # print("boundary margin", "minx=", minX,"minY=", minY,"maxX=",maxX,"maxY=",maxY)

        validWithinBoundaryBlankSpots={}

        for possibleCellsKey, _ in self.blankSpots.items():  #possible actions
                r,c = possibleCellsKey[0], possibleCellsKey[1]

                if r>=minX and r<=maxX and c>=minY and c<=maxY:
                    validWithinBoundaryBlankSpots[(r,c)] = [r,c]
        # pprint(self.board)
        # print("Empty cells selected within boundary", validWithinBoundaryBlankSpots)
        #TODO sort the blank spots
        # self.sortingTheBlankSpots(validWithinBoundaryBlankSpots)
        # return validWithinBoundaryBlankSpots
        return self.sortingTheBlankSpots(validWithinBoundaryBlankSpots, player)

    def calculateFavourablePlayer(self, block, patternhashmap, player):
        
        # print("CALCULATING SCORE for PATTERNS OF LENGTH", len(patternhashmap), patternhashmap)

        #(white, black, .)

        if player==whitePlayer:
            patternScoreHashmap = {
                (4,0,1): {('ww.ww', 'www.w', '.wwww', 'wwww.', 'w.www'): math.pow(10,20)},
                (0,4,1): {('bb.bb' , 'bbb.b','.bbbb', 'bbbb.', 'b.bbb'): -math.pow(10,15)},
                # (3,1,1): {('.wwwb', 'w.wwb', 'ww.wb', 'bwww.', 'bww.w', 'bw.ww', 'b.www'): math.pow(10,1)},
                # (1,3,1): {('.bbbw', 'b.bbw', 'bb.bw', 'wbbb.', 'wbb.b', 'wb.bb', 'w.bbb'): math.pow(10,1)},
                (3,0,2): { tuple(set(["".join(x) for x in list(permutations('www..'))])): math.pow(10,6)},
                (0,3,2): {tuple(set(["".join(x) for x in list(permutations('bbb..'))])): -math.pow(10,4)},
                #changed 10,3 to 10,2 for ww...
                (2,0,3): { tuple(set(["".join(x) for x in list(permutations('ww...'))])): math.pow(10,3)},
                (0,2,3): { tuple(set(["".join(x) for x in list(permutations('bb...'))])): -math.pow(5,1)},
                (1,0,4): { tuple(set(["".join(x) for x in list(permutations('w...'))])): math.pow(10,1)},
                (0,1,4): { tuple(set(["".join(x) for x in list(permutations('b...'))])): -math.pow(1,1)},
                (1,1,3): { tuple(set(["".join(x) for x in list(permutations('wb...'))])): math.pow(1,1)},
                (2,1,2): { tuple(set(["".join(x) for x in list(permutations('wbw..'))])): math.pow(3,1)},
                (1,2,2): { tuple(set(["".join(x) for x in list(permutations('bwb..'))])): -math.pow(1,1)},
            
                }
            
        else: #player is black
            # patternScoreHashmap = {
            #     (4,0,1): {('ww.ww', 'www.w', '.wwww', 'wwww.', 'w.www'): -math.pow(10,15)},
            #     (0,4,1): {('bb.bb' , 'bbb.b','.bbbb', 'bbbb.', 'b.bbb'): -math.pow(10,20)},
            #     (1,3,1): {('.bbbw', 'b.bbw', 'bb.bw', 'wbbb.', 'wbb.b', 'wb.bb', 'w.bbb'): -math.pow(10,1)},
            #     (3,1,1): {('.wwwb', 'w.wwb', 'ww.wb', 'bwww.', 'bww.w', 'bw.ww', 'b.www'): -math.pow(10,1)},
            #     (3,0,2): { tuple(set(["".join(x) for x in list(permutations('www..'))])): -math.pow(10,4)},
            #     (0,3,2): {tuple(set(["".join(x) for x in list(permutations('bbb..'))])): -math.pow(10,6)},
            #     (2,0,3): { tuple(set(["".join(x) for x in list(permutations('ww...'))])): -math.pow(5,1)},
            #     (0,2,3): { tuple(set(["".join(x) for x in list(permutations('bb...'))])): -math.pow(10,1)},
            #     (1,0,4): { tuple(set(["".join(x) for x in list(permutations('w...'))])): -math.pow(1,1)},
            #     (0,1,4): { tuple(set(["".join(x) for x in list(permutations('b...'))])): -math.pow(2,1)},
            #     (1,1,3): { tuple(set(["".join(x) for x in list(permutations('wb...'))])): -math.pow(1,1)},
            #     (2,1,2): { tuple(set(["".join(x) for x in list(permutations('wbw..'))])): -math.pow(3,1)},
            #     (1,2,2): { tuple(set(["".join(x) for x in list(permutations('bwb..'))])): -math.pow(5,1)},
            
            #     }

            patternScoreHashmap = {
                (4,0,1): {('ww.ww', 'www.w', '.wwww', 'wwww.', 'w.www'): math.pow(10,15)},
                (0,4,1): {('bb.bb' , 'bbb.b','.bbbb', 'bbbb.', 'b.bbb'): -math.pow(10,20)},
                # (1,3,1): {('.bbbw', 'b.bbw', 'bb.bw', 'wbbb.', 'wbb.b', 'wb.bb', 'w.bbb'): -math.pow(10,1)},
                # (3,1,1): {('.wwwb', 'w.wwb', 'ww.wb', 'bwww.', 'bww.w', 'bw.ww', 'b.www'): -math.pow(10,1)},
                (3,0,2): { tuple(set(["".join(x) for x in list(permutations('www..'))])): math.pow(10,4)},
                (0,3,2): {tuple(set(["".join(x) for x in list(permutations('bbb..'))])): -math.pow(10,6)},
                (2,0,3): { tuple(set(["".join(x) for x in list(permutations('ww...'))])): math.pow(5,1)},
                #changed 10,3 to 10,2 for bb...
                (0,2,3): { tuple(set(["".join(x) for x in list(permutations('bb...'))])): -math.pow(10,3)},
                (1,0,4): { tuple(set(["".join(x) for x in list(permutations('w...'))])): math.pow(1,1)},
                (0,1,4): { tuple(set(["".join(x) for x in list(permutations('b...'))])): -math.pow(10,1)},
                (1,1,3): { tuple(set(["".join(x) for x in list(permutations('wb...'))])): -math.pow(1,1)},
                (2,1,2): { tuple(set(["".join(x) for x in list(permutations('wbw..'))])): math.pow(1,1)},
                (1,2,2): { tuple(set(["".join(x) for x in list(permutations('bwb..'))])): -math.pow(3,1)},
                
                }
        
        score = {4:math.pow(10,10) if player == whitePlayer else math.pow(10,7), 
                -4: math.pow(10,10) if player == blackPlayer else -2000, -3:-10, 3:10, -2:-5, 2:5, -1:-1, 1:1}
        
        calculate_score=0

        


        #print(block)

        count_number_of_white_trias=0
        count_number_of_black_trias=0
        count_number_of_white_captured=0
        count_number_of_black_captured=0

        lisofblacktrias=[]
        lisofwhitetrias=[]
        listofwhitecaptured = []
        listofblackcaptured = []
 
        # print("HASHMAP PATTERNS:----", patternhashmap, "\n")
        # print("SCORE HASHMAP", patternScoreHashmap, "\n")
        # ".wwb.","bww..",".bww.", ".wbb.", ".wwbb","bww.b","bbww.", "b.wwb"

       
        if player==blackPlayer:
            calculate_score+= -math.pow(10,20)  if self.blackCapture >=4 else -math.pow(10,4.5)*self.blackCapture
        
        elif player==whitePlayer:
            calculate_score+= math.pow(10,20)  if self.whiteCapture >=4 else math.pow(10,4.5)*self.whiteCapture

    
        for key, value in patternhashmap.items():
            if "." in key:
                w,b,d = key.count('w'), key.count('b'), key.count('.')
                # print("pattern: ", key, " (w,b,d):", (w,b,d), )
                if (w,b,d) in patternScoreHashmap:
                    calculate_score = calculate_score + (list(patternScoreHashmap[(w,b,d)].values())[0])*value
                    # print("------each pattern score", calculate_score, patternScoreHashmap[(w,b,d)], "\n")

        
        '''print(lisofwhitetrias, len(lisofwhitetrias),lisofblacktrias, len(lisofblacktrias), sep="\n")
        print(count_number_of_white_trias, count_number_of_black_trias)
        
        print("BLOCK :", block)
        for key, value in block.items():
            #print("Key : ", key, "value : ", value)
            calculate_score+=(score[key]*value if key in score else 0)
        
        for key, value in block.items():
            if key==4:
                calculate_score+=score[key]*value
            elif key==-4:
                calculate_score+=score[key]*value
        
        
        calculate_score = calculate_score + (count_number_of_white_trias - count_number_of_black_trias)*30 + (count_number_of_black_captured - count_number_of_white_captured)*30

        print(block, calculate_score)
        print("BLOCK = ", block, " ; SCORE = ", calculate_score)'''

        return calculate_score
        

    def calculateDepth(self, player, goaltestscore, timeleft):
        global MAXDEPTH
        if len(self.blackPieces)<=3 or len(self.whitePieces)<=3 or float(timeleft)<15 or -math.inf<=goalscorestart<=-math.pow(10,14) or math.inf>=goalscorestart>=math.pow(10,14):
            if player == whitePlayer :
                MAXDEPTH = 1
            else:
                MAXDEPTH = 2
        
        elif player == whitePlayer:
            MAXDEPTH = 3

        else:
            MAXDEPTH = 4
        print("MAXDEPTH", MAXDEPTH)

    
    def generatingPatterns(self):
        chars = "wb."
        word_length = 5

        # Generate all possible combinations of the characters for the given word length
        combinations = list(itertools.product(chars, repeat=word_length))

        # Filter out patterns without at least one "."
        filtered_combinations = [combo for combo in combinations if "." in combo]

        patterns = {}
        # Print the patterns
        for combo in filtered_combinations:
            patterns["".join(combo)] = 1

        return patterns
    

        
    #check if 5 vertical/horizontal/vertical line is possible and if yes by whom. If draw return that else return False
    def check5line(self, player):
        block = {}
        pattern_hashmap={}
        mappingInt2Char={0:".", -1:"b", 1:"w"}
        blocktrias = {}

        #checking diagonal line which is right->left
        for i in range(15):
            for j in range(4,19):

                list5 = [self.board[i+k][j-k] for k in range(5)]
                # print(list5)
                sumPieces = sum(list5)
                if sumPieces==-5:
                    return blackWins #black wins
                elif sumPieces==5:
                    return whiteWins #white wins
                else:
                    pattern=""
                    for ch in list5:
                        pattern+=mappingInt2Char[ch]
                
                    block[sumPieces] = 1 if sumPieces not in block else block[sumPieces] + 1
                    pattern_hashmap[pattern] = 1 if pattern not in pattern_hashmap else pattern_hashmap[pattern] + 1

        

        for i in range(15):
            for j in range(15):
                list5 = [self.board[i+k][j+k]for k in range(5)]
                sumPieces = sum(list5)
                if sumPieces==-5:
                    return blackWins #black wins
                elif sumPieces==5:
                    return whiteWins #white wins
                else:
                    pattern=""
                    for ch in list5:
                        pattern+=mappingInt2Char[ch]
                    block[sumPieces] = 1 if sumPieces not in block else block[sumPieces] + 1
                    pattern_hashmap[pattern] = 1 if pattern not in pattern_hashmap else pattern_hashmap[pattern] + 1
                
        #checking vertical line
        for i in range(15):
            for j in range(19):
                list5 = [self.board[i+k][j] for k in range(5)]
                sumPieces = sum(list5)
                if sumPieces==-5:
                    return blackWins #black wins
                elif sumPieces==5:
                    return whiteWins #white wins
                else:
                    pattern=""
                    for ch in list5:
                        pattern+=mappingInt2Char[ch]
                    block[sumPieces] = 1 if sumPieces not in block else block[sumPieces] + 1
                    pattern_hashmap[pattern] = 1 if pattern not in pattern_hashmap else pattern_hashmap[pattern] + 1

        #checking horizontal line
        for i in range(19):
            for j in range(15):
                list5 = [self.board[i][j+k] for k in range(5)]
                sumPieces = sum(list5)
                if sumPieces==-5:
                    return blackWins #black wins
                elif sumPieces==5:
                    return whiteWins #white wins
                else:
                    pattern=""
                    for ch in list5:
                        pattern+=mappingInt2Char[ch]
                    block[sumPieces] = 1 if sumPieces not in block else block[sumPieces] + 1
                    pattern_hashmap[pattern] = 1 if pattern not in pattern_hashmap else pattern_hashmap[pattern] + 1
        
        
        # print("Patterns : ", pattern_hashmap)
        if len(self.blankSpots)==0:
            # print("draw situtation")
            return draw
        return self.calculateFavourablePlayer(block, pattern_hashmap, player)

                
    #function to just return the possible neighbours, given index i,j
    def listOfNeighbours(self,i,j):
        neighbours = {(i-3,j-3):[[i-2,j-2],[i-1,j-1]],
                      (i-3,j):[[i-2,j],[i-1,j]], 
                      (i-3,j+3):[[i-2,j+2],[i-1,j+1]], 
                      (i,j-3):[[i,j-2],[i,j-1]], 
                      (i,j+3):[[i,j+2],[i,j+1]], 
                      (i+3,j-3):[[i+2,j-2],[i+1,j-1]], 
                      (i+3,j):[[i+2,j],[i+1,j]], 
                      (i+3,j+3):[[i+2,j+2],[i+1,j+1]]
                      }
        return neighbours
    

    #function to return the pairs which can be captured by a given player given position i,j
    def listOfCapturePairs(self, i, j, player):
        hashMapBetweenNeighbours = self.listOfNeighbours(i,j)
        validhashMapBetweenNeighbours = {}
        for key,value in hashMapBetweenNeighbours.items():
            r,c = key[0], key[1]

            if r>=0 and r<=18 and c>=0 and c<=18 and self.board[r][c]==player: #if in boundary and if the player is same
                betweenchild1_r, betweenchild1_c = value[0]
                betweenchild2_r, betweenchild2_c = value[1]

                oppositeplayer= (-1)*player

                #if the between cells match opposite player
                if(self.board[betweenchild1_r][betweenchild1_c]==oppositeplayer and self.board[betweenchild2_r][betweenchild2_c]==oppositeplayer):
                    validhashMapBetweenNeighbours[key]=value

        # print("validhashMapBetweenNeighbours", validhashMapBetweenNeighbours)
        return validhashMapBetweenNeighbours
    

    #function to update the board when making a move
    def updateMove(self, i,j, player):
        
        self.board[i][j]=player  
        # print("inside updateMove", self.blankSpots, "EMPTY CELL=",(i,j), "player=", player)
        del self.blankSpots[(i,j)] #updating the blankspots hashmap

        capturePairs = self.listOfCapturePairs(i,j, player)
        for key,value in capturePairs.items():
            
            betweenchild1_r, betweenchild1_c = value[0]
            betweenchild2_r, betweenchild2_c = value[1]
            self.board[betweenchild1_r][betweenchild1_c] = 0
            self.board[betweenchild2_r][betweenchild2_c] = 0

            # print("captured", capturePairs)

            if player==1: #white piece is playing
                self.whiteCapture+=1 #black pair is captured by white
            elif player==-1: #black piece is playing
                self.blackCapture+=1 #white pair is captured by black
        

    #Goal Test definition
    def goalTest(self, player):
        score = self.check5line(player)
        # print("GOALTEST SCORE", score)
        if score in [blackWins, whiteWins, draw]:
            return score
        elif self.whiteCapture==5:
            return whiteWins
        elif self.blackCapture==5:
            return blackWins
        
        return score

def assignPlayerColor(playerColor):
    if playerColor=='.':
        return 0
    elif playerColor=='b': #black piece
        return -1
    else:
        return 1


def maxValue(penteBoardObj:penteBoard, depth, player, alpha, beta, prev_move, pruning=True):
    # print("Max block", depth)
    bestAction, bestDepth = None, math.inf
    v = -math.inf

    terminalTest = penteBoardObj.goalTest(player)
    # print("Depth : ", depth, ": Terminal test = ", terminalTest)
    if terminalTest in [blackWins, whiteWins, draw]:
        #print("terminal test in max block ", terminalTest, player)
        return bestAction, terminalTest, depth

    if depth==MAXDEPTH:
        return bestAction, terminalTest, depth

    validActions = []
    if player==whitePlayer and len(penteBoardObj.whitePieces)==1 and len(penteBoardObj.blackPieces)==1 and penteBoardObj.blackCapture==0 and penteBoardObj.whiteCapture==0: #white is making the second move after black move
        
        i,j = 9,9
        for possibleCellsKey, _ in penteBoardObj.blankSpots.items():  #possible actions
            r,c = possibleCellsKey[0], possibleCellsKey[1]
            if abs(i-r) in [3,4] and abs(j-c) in [3,4]:
                validActions.append((r,c))
        print("Valid Actions for white player at the second move", validActions)

    else:
        # validActions = penteBoardObj.blankSpots
        validActions = penteBoardObj.getBlankSpotsWithinBoundary(player)

    scoreByAction = {}
    for possibleCellsKey in validActions[0:20]:
        new_penteBoardObj = penteBoard(penteBoardObj.board, penteBoardObj.whiteCapture, penteBoardObj.blackCapture)
        new_penteBoardObj.updateMove(possibleCellsKey[0], possibleCellsKey[1], whitePlayer)
        action, actionvalue, depthvalue = minValue(new_penteBoardObj, depth+1, -player, alpha, beta, possibleCellsKey)
        
        # print("Depth : ", depth, ", previous move :", None, ": current move played by ", player, " ", row_name[possibleCellsKey[0]]+col_name[possibleCellsKey[1]], "with score as: ", actionvalue)

        scoreByAction[possibleCellsKey] = (actionvalue, depthvalue)
        # print("Score after making move by white", possibleCellsKey) if depth==0 else None
        if actionvalue>v or (actionvalue==v and depthvalue<=bestDepth):
            v = actionvalue
            bestDepth = depthvalue
            bestAction = possibleCellsKey

        # v, callbackDepth = max(v, minValue(new_penteBoardObj, depth+1, player, alpha, beta))
        
        if pruning and v>=beta: return bestAction, v, bestDepth
        alpha = max(alpha,v)

    # print(scoreByAction) if depth==0 else None
    return bestAction, v, bestDepth



def minValue(penteBoardObj:penteBoard, depth, player, alpha, beta, prev_move, pruning=True):
    # print("Min block", depth)
    bestAction, bestDepth = None, math.inf
    v = math.inf

    terminalTest = penteBoardObj.goalTest(player)
    if terminalTest in [blackWins, whiteWins, draw]:
        return bestAction, terminalTest, depth
    
    if depth==MAXDEPTH:
        return bestAction, terminalTest, depth
    
    scoreByAction = {}

    validActions = penteBoardObj.getBlankSpotsWithinBoundary(player)
    for possibleCellsKey in validActions[0:20]:
        # print("Depth : ", depth, ": move played by black", possibleCellsKey)
        new_penteBoardObj = penteBoard(penteBoardObj.board, penteBoardObj.whiteCapture, penteBoardObj.blackCapture)
        new_penteBoardObj.updateMove(possibleCellsKey[0], possibleCellsKey[1], blackPlayer)
        _ , actionvalue, depthvalue = maxValue(new_penteBoardObj, depth+1, -player, alpha, beta, possibleCellsKey)
        # if(prev_move == (11, 15)):
        # print("Depth : ", depth, ", previous move :", None, ": current move played by ", player, " ", row_name[possibleCellsKey[0]]+col_name[possibleCellsKey[1]], "with score as: ", actionvalue)
        scoreByAction[possibleCellsKey] = (actionvalue, depthvalue)
        if actionvalue<v or (actionvalue==v and depthvalue<=bestDepth):
            v = actionvalue
            bestDepth = depthvalue
            bestAction = possibleCellsKey
        # print("Score By action",scoreByAction) if depth==0 else None
        # action, v, bestDepth= min(v, maxValue(new_penteBoardObj, depth+1, player, alpha, beta))
        if pruning and v<=alpha: return bestAction, v, bestDepth
        beta = min(beta,v)
    
    # print(scoreByAction) if depth==0 else None
    return bestAction, v, bestDepth

def minmax_decision(penteBoardObj:penteBoard, player):
    validActions = {}

    if player==whitePlayer and len(penteBoardObj.whitePieces)==0 and len(penteBoardObj.blackPieces)==0: #white is making the first move in an empty board
        possibleCellsKey = [9,9] #place at center of the board
        penteBoardObj.board[9][9] = whitePlayer
        penteBoardObj.whitePieces = 1
        del penteBoardObj.blankSpots[(9,9)]
        return (9,9), None, None
    
    
    if player==whitePlayer:
        # print("Actions possible", validActions)
        return maxValue(penteBoardObj, 0, player, ALPHA, BETA, None)
        # scoreByAction = {}
        
    elif player==blackPlayer:
        return minValue(penteBoardObj, 0, player, ALPHA, BETA, None)
        

def plot_board(board_arr, latest_move, player, is_terminal):
    
    w, h = 30, 30
    cell_colors = [["#90EE90" for i in range(19)] for i in range(19)] if is_terminal else [["w" for i in range(19)] for i in range(19)]    
    
    if(player == blackPlayer):
        cell_colors[latest_move[0]][latest_move[1]] = "#FF0000"
    elif(player == whitePlayer):
        cell_colors[latest_move[0]][latest_move[1]] = "#FFFF00"
        
    plt.figure(1, figsize=(w, h))
    tb = plt.table(cellText=board_arr, loc=(0,0), cellLoc='center', 
                   cellColours = cell_colors, colLabels = col_name, rowLabels = row_name)
    tb.auto_set_font_size(False)
    tb.set_fontsize(20)
    tc = tb.properties()['children']
    for cell in tc: 
        cell.set_height(1.0/24)
        cell.set_width(1.0/24)
    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


with open("input.txt") as inputfile:
    player = assignPlayerColor(inputfile.readline().strip().lower()[0])
    #whitecapture number of pieces captured by white
    #blackCapture number of pieces captured by black
    timeleft = inputfile.readline().strip()
    whiteCapture, blackCapture = list(map(int, inputfile.readline().strip().split(",")))
    whiteCapture, blackCapture = whiteCapture/2, blackCapture/2
    board = []
    for _ in range(19):
        board.append(list(inputfile.readline().strip()))
    
    penteBoardObj = penteBoard(board, whiteCapture, blackCapture)
    goalscorestart = penteBoardObj.goalTest(player)
    penteBoardObj.calculateDepth(player, goalscorestart, timeleft)

    start_time = time.time()
    bestAction, bestValue, bestDepth = minmax_decision(penteBoardObj, player)
    end_time = time.time()
    if bestAction:
        final_move = row_name[bestAction[0]]+col_name[bestAction[1]]
    else:
        final_move = ''
        print("GAME OVER")
    
    # print("Captured", penteBoardObj.whiteCapture, penteBoardObj.blackCapture)
    print("bestAction, bestValue, bestDepth", final_move, bestValue, bestDepth)
    print("Time taken:", end_time-start_time)

    fopen = open("output.txt", "w")
    fopen.write(final_move)
    fopen.close()

    # plot_board(board, bestAction, player, 0)

    