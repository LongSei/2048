import math

def Heuristic(self): 
    score = 0
    First_Condition_Constant = 8192
    Second_Condition_Constant = 20
    Third_Condition_Constant = 10
    
    Largest_Cell_Value = 0
    for row in range(0, self.size): 
        for col in range(0, self.size): 
            Largest_Cell_Value = max(Largest_Cell_Value, self.board[row][col])
            
    for row in range(0, self.size): 
        for col in range(0, self.size): 
            # Add Score for the empty cell
            if (self.board[row][col] == 0): 
                score += First_Condition_Constant
            else: 
                # Minus Score for the distance of each cell to the border
                distance = min(min(row, self.size - 1 - row), min(col, self.size - 1 - col))
                score -= Third_Condition_Constant * distance * self.board[row][col]
                
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
                score -= Second_Condition_Constant * abs(self.board[row][col] - self.board[row][col - 1])
            if (self.board[row][col] == 0 and self.board[row - 1][col] == 0): 
                score -= Second_Condition_Constant * abs(self.board[row][col] - self.board[row - 1][col])

    return score