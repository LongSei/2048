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
            game.game_over = True
    def move_left(self,col):
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

if __name__ == '__main__':
    game = game_2048()
    game.fill_cell()
    game.fill_cell()

    while(not game.game_over):
        prev_state = game.board
        di = int(input()) #direction
        game.move(di)
        game.fill_cell()
        print(game.board)