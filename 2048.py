import numpy as np

from minimax_long import getMoveMinimax

        
class game_2048():
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=np.int64)
        self.game_over = False

    def fill_cell(self):
        i, j = (self.board == 0).nonzero()
        if i.size > 1:
            rnd = np.random.randint(0, i.size - 1)
            self.board[i[rnd], j[rnd]] = ((np.random.random() > .9) + 1)
        elif i.size == 1:
            self.board[i[0], j[0]] = ((np.random.random() > .9) + 1)
        else:
            self.game_over = True

    def move_left(self, col):
        new_col = np.zeros((4), dtype=np.int64)
        j = 0
        previous = None
        for i in range(col.size):
            if col[i] != 0:  # number different from zero
                if previous == None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_col[j] = col[i]+1
                        j += 1
                        previous = None
                    else:
                        new_col[j] = previous
                        j += 1
                        previous = col[i]
        if previous != None:
            new_col[j] = previous
        return new_col

    def move(self, direction):
        # 0: left, 1: up, 2: right, 3: down
        new_board = np.rot90(self.board, direction)
        cols = [self.board[i, :] for i in range(4)]
        new_board = np.array([self.move_left(col) for col in cols])
        new_board = np.rot90(self.board, -direction)
        if np.array_equal(new_board,self.board):
            return False
        self.board = new_board
        return True

    # Heuristic function
    def R(self):
        res = 0
        res = res + (16 - self.board.nonzero()[0].size)*4096
        tmp = self.board.argmax()
        check_corner = (self.board == [tmp])
        for (i, j) in [(0, 0), (0, 3), (3, 0), (3, 3)]:
            if check_corner[i, j] == 1:
                res = res + 1e5
                break
        return res


    # Greedy algorithm
    def greedy(self):
        while not self.game_over:
            max_R = -1e9
            current_state = self.board
            best_move = None
            for dir in [0, 1, 2, 3]:
                self.move(dir)
                if(self.R() > max_R):
                    best_move = dir
                    max_R = self.R()
                self.board = current_state
            self.move(best_move)
            self.fill_cell()
            # print(self.board)

    def getMoveMinimax(self, alpha = -1e9, beta = 1e9, computer_or_person = True, depth = 5): 
        if (depth == 0 or self.game_over == True): 
            return (self.R(), self.board)
        
        if (computer_or_person == True): 
            bestState= None
            for direction in range(0, 4): 
                cloneBoard = self.board.copy()
                self.move(direction)
                if np.array_equal(cloneBoard, self.board): 
                    self.board = cloneBoard
                    continue
                result, state = self.getMoveMinimax(self, alpha, beta, 0, depth - 1)
                if (result > alpha): 
                    alpha = max(alpha, result)
                    bestState = self.board
                if (beta <= alpha): 
                    break
                self.board = cloneBoard
            return (alpha, bestState)
        
        else: 
            terminate = False
            worstState = None
            for row in range(0, self.size): 
                if (terminate == True): 
                    break
                for col in range(0, self.size): 
                    if (self.board[row,col] == 0): 
                        cloneBoard = self.board.copy()
                        self.board[row,col] = 1
                        result, state = self.getMoveMinimax(self, alpha, beta, 1, depth - 1)
                        beta = min(beta, result)
                        if (beta <= alpha): 
                            terminate = True
                            worstState = self.board
                        self.board = cloneBoard
                        
                        cloneBoard = self.board.copy()
                        self.board[row,col] = 2
                        result, state = self.getMoveMinimax(self, alpha, beta, 1, depth - 1)
                        beta = min(beta, result)
                        if (beta <= alpha): 
                            terminate = True
                            worstState = self.board
                        self.board = cloneBoard
            return (beta, worstState)






# main
game = game_2048()
game.fill_cell()
game.fill_cell()
while( not game.game_over):
    score, game.board = game.getMoveMinimax()
print(game.board)
#  main loop
# while(not game.game_over):
#     print(game.board)
#     prev_state = game.board
#     di = int(input())  # direction
#     game.move(di)
#     if not np.array_equal(prev_state, game.board):
#         game.fill_cell()
