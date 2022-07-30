from tkinter.messagebox import NO
import numpy as np

class game_2048():
    def __init__(self,board) -> None:
        self.board = board
        self.game_over = False
    def move_(self, dir):       
        next_move = move(self.board, dir)
        if np.array_equal(next_move,self.board):
            return False
        self.board = next_move
        self.board = random_fill_cell(self.board)
        if(self.board == None):
            self.game_over = True
            return False
        return True



def random_fill_cell(board):
    i, j = (board == 0).nonzero()
    if i.size > 1:
        rnd = np.random.randint(0, i.size - 1)
        board[i[rnd], j[rnd]] = ((np.random.random() > .9) + 1)
    elif i.size == 1:
        board[i[0], j[0]] = ((np.random.random() > .9) + 1)
    else:
        return None
    return board

def move_left(row):
    new_row = np.zeros((4))
    j = 0
    previous = None
    for i in range(row.size):
        if row[i] != 0:  # number different from zero
            if previous == None:
                previous = row[i]
            else:
                if previous == row[i]:
                    new_row[j] = row[i]+1
                    j += 1
                    previous = None
                else:
                    new_row[j] = previous
                    j += 1
                    previous = row[i]
    if previous != None:
        new_row[j] = previous
    return new_row

def move(board, dir):
    # 0: left, 1: up, 2: right, 3: down
    new_board = np.rot90(board, dir)
    rows = [board[i, :] for i in range(4)]
    new_board = np.array([move_left(row) for row in rows])
    new_board = np.rot90(board, -dir)
    if np.array_equal(new_board,board):
        return None
    return new_board