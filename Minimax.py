from Heuristic import Heuristic
import math
import random

def getMoveMinimax(self, alpha, beta, computer_or_person, depth): 
    if (depth == 0): 
        return Heuristic(self);
    
    if (computer_or_person == True): 
        bestMove = 0
        for direction in range(0, 4): 
            cloneBoard = self.board.copy()
            self.move(direction)
            if ((cloneBoard == self.board).all()): 
                self.board = cloneBoard
                continue
            result = getMoveMinimax(self, alpha, beta, 0, depth - 1)
            if (result > alpha): 
                alpha = max(alpha, result)
                bestMove = direction
            if (beta <= alpha): 
                break
            self.board = cloneBoard
        return bestMove
    
    else: 
        terminate = False
        for row in range(0, self.size): 
            if (terminate == True): 
                break
            for col in range(0, self.size): 
                if (self.board[row][col] == 0): 
                    cloneBoard = self.board.copy()
                    self.board[row][col] = 2
                    result = getMoveMinimax(self, alpha, beta, 1, depth - 1)
                    beta = min(beta, result)
                    if (beta <= alpha): 
                        terminate = True
                    self.board = cloneBoard
                    
                    cloneBoard = self.board.copy()
                    self.board[row][col] = 4
                    result = getMoveMinimax(self, alpha, beta, 1, depth - 1)
                    beta = min(beta, result)
                    if (beta <= alpha): 
                        terminate = True
                    self.board = cloneBoard
        return beta