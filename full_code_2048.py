import numpy as np


class game_2048():
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=np.int64)
        self.game_over = False
        self.size = 4

    def fill_cell(self):
        row, col = (self.board == 0).nonzero()
        if row.size > 1:
            rnd = np.random.randint(0, row.size - 1)
            self.board[row[rnd], col[rnd]] = ((np.random.random() > .9) + 1)
        elif row.size == 1:
            self.board[row[0], col[0]] = ((np.random.random() > .9) + 1)
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
        self.board = np.rot90(self.board, direction)
        # print(self.board)
        cols = [self.board[i, :] for i in range(4)]
        self.board = np.array([self.move_left(col) for col in cols])
        # print(self.board)
        self.board = np.rot90(self.board, -direction)


def Heuristic(self):
    score = 0
    First_Condition_Constant = 8192
    Second_Condition_Constant = 20
    Third_Condition_Constant = 10

    # Largest_Cell_Value = 0
    # for row in range(0, self.size):
    #     for col in range(0, self.size):
    #         Largest_Cell_Value = max(Largest_Cell_Value, self.board[row][col])
    Largest_Cell_Value = self.board.max()
    for row in range(0, self.size):
        for col in range(0, self.size):
            # Add Score for the empty cell
            if (self.board[row][col] == 0):
                score += First_Condition_Constant
            else:
                # Minus Score for the distance of each cell to the border
                distance = min(min(row, self.size - 1 - row),
                               min(col, self.size - 1 - col))
                score -= Third_Condition_Constant * \
                    distance * self.board[row][col]

                # Add Score if the largest cell is place at the corner
                if (self.board[row][col] == Largest_Cell_Value):
                    xBorder = (row == 0 or row == self.size - 1)
                    yBorder = (col == 0 or col == self.size - 1)
                    if (xBorder and yBorder):
                        score += First_Condition_Constant
                    elif (xBorder or yBorder):
                        score += First_Condition_Constant // 2

    for row in range(0, self.size):
        for col in range(0, self.size):
            if (self.board[row][col] == 0 and self.board[row][col - 1] == 0):
                score -= Second_Condition_Constant * \
                    abs(self.board[row][col] - self.board[row][col - 1])
            if (self.board[row][col] == 0 and self.board[row - 1][col] == 0):
                score -= Second_Condition_Constant * \
                    abs(self.board[row][col] - self.board[row - 1][col])

    return score


# def Heuristic(self):
#     res = 0
#     res = res + (16 - self.board.nonzero()[0].size)*4096
#     tmp = self.board.max()
#     check_corner = (self.board == [tmp])
#     for (i, j) in [(0, 0), (0, 3), (3, 0), (3, 3)]:
#         if check_corner[i, j] == 1:
#             res = res + 1e5
#             break
#     return res

def getMoveMinimax(self, alpha, beta, computer_or_person, depth):
    if (depth == 0):
        return {"move": -1, "score": Heuristic(self)}

    if (computer_or_person == True):
        bestMove = {"move": -1, "score": alpha}
        for direction in range(0, 4):
            cloneBoard = self.board.copy()
            self.move(direction)
            if ((cloneBoard == self.board).all()):
                self.board = cloneBoard
                continue
            result = getMoveMinimax(self, alpha, beta, 0, depth - 1)
            if (result["score"] > alpha):
                alpha = max(alpha, result["score"])
                bestMove = {"move": direction, "score": alpha}
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
                    self.board[row][col] = 1
                    result = getMoveMinimax(self, alpha, beta, 1, depth - 1)
                    beta = min(beta, result["score"])
                    if (beta <= alpha):
                        terminate = True
                    self.board = cloneBoard

                    cloneBoard = self.board.copy()
                    self.board[row][col] = 2
                    result = getMoveMinimax(self, alpha, beta, 1, depth - 1)
                    beta = min(beta, result["score"])
                    if (beta <= alpha):
                        terminate = True
                    self.board = cloneBoard
        return {"move": -1, "score": beta}


def getMoveExpectimax(self, turn, depth):
    if depth == 0:
        return {"move": -1, "score": Heuristic(self)}
    if turn == True:
        bestScore = -1e9
        bestMove = {"move": -1, "score": bestScore}
        for direction in range(0, 4):
            cloneBoard = self.board.copy()
            self.move(direction)
            if ((cloneBoard == self.board).all()):
                self.board = cloneBoard
                continue
            result = getMoveExpectimax(self, 0, depth - 1)
            if (result["score"] > bestScore):
                bestScore = max(bestScore, result["score"])
                bestMove = {"move": direction, "score": bestScore}
            self.board = cloneBoard
        return bestMove
    else:
        expectedValue = 0
        row, col = (self.board == 0).nonzero()
        empty_tile = row.size
        for r in row:
            for c in col:
                cloneBoard = self.board.copy()
                self.board[r][c] = 1
                result = getMoveExpectimax(self, 1, depth - 1)
                expectedValue = expectedValue + result['score']*0.9/empty_tile
                self.board = cloneBoard

                cloneBoard = self.board.copy()
                self.board[r][c] = 2
                result = getMoveExpectimax(self, 1, depth - 1)
                expectedValue = expectedValue + result['score']*0.1/empty_tile
                self.board = cloneBoard
    return {"move": -1, "score": expectedValue}


with open("test2.txt", "w") as external_file:
    game = game_2048()
    game.fill_cell()
    game.fill_cell()
    while(not game.game_over):
        # print(game.board, file=external_file)
        best_move = getMoveExpectimax(game, True, 3)['move']
        direction = ["Left", 'Up', 'Right', 'Down']
        # print(direction[best_move], file=external_file)
        game.move(best_move)
        game.fill_cell()

    print(game.board, file=external_file)
    external_file.close()
