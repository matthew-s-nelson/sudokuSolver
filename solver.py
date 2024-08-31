


class sudokuBoard:
    def __init__(self, board):
        self.board = board
        # self.columns = [self.get_column(x) for x in range(9)]
    
    # Creates the lists of columns for the class
    def get_column(self, x):
        column = []
        for row in self.board:
            column.append(row[x])
        return column

    # Checks if a box in the grid is empty (needs solving)
    def is_empty(self, x, y):
        return self.board[y][x] is None

    # Gets the value of a box in the grid
    def get_box(self, x, y):
        return self.board[y][x]
    
    # Sets the box at the x, y coordinate to the val passed in
    def set_box(self, x, y, val):
        self.board[y][x] = val

    def get_grid(self, x, y):
        x_min = x//3
        y_min = y//3
        grid = [self.get_box(x, y) for x in range(3*x_min, 3*(x_min+1)) for y in range(3*y_min, 3*(y_min+1))]
        return grid

    # Returns the first empty box on the grid. Returns 9,9 if there's no empty boxes
    def find_empty(self):
        for y in range(9):
            for x in range(9):
                if self.is_empty(x, y):
                    return x, y
        return 9,9
    
    def solve(self):
        x, y = self.find_empty()

        if x == 9 and y == 9:
            return True
        
        for val in range(1, 10):
            if val not in self.get_column(x) and val not in self.board[y] and val not in self.get_grid(x,y):
                self.set_box(x, y, val)
                
                # Checks if the board can be solved with that new value
                if self.solve():
                    return True
                
                # If it can't be solved yet, reset to try the next number
                self.set_box(x, y, None)

        # Board can't be solved.
        return False
    
    def get_board(self):
        return self.board



    def __str__(self):
        string = ''
        for row in self.board:
            string += f'{row}\n'
        return string











board_solved= [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

board_easy= [
    [None, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

board_image2 = [
    [None, 3, None, None, None, None, None, None, None],
    [None, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, None],
    [4, None, None, None, None, 3, None, None, 1],
    [None, None, None, None, 2, None, None, None, None],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, None, None, None, 7, None]
]

board3 = [
    [5, 3, None, None, 7, None, None, None, None],
    [6, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, 3],
    [4, None, None, 8, None, 3, None, None, 1],
    [7, None, None, None, 2, None, None, None, 6],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, 8, None, None, 7, 9]
]

board4 = [
    [None, None, None, None, 2, None, None, None, None],
    [None, None, 4, None, None, None, None, 3, None],
    [8, 5, None, None, None, None, None, None, None],
    [None, None, 2, None, None, None, None, 8, None],
    [None, None, None, None, None, 1, 9, None, None],
    [None, 4, None, None, None, None, None, None, 5],
    [3, None, None, None, None, None, 7, None, None],
    [None, None, None, None, 5, None, None, None, None],
    [None, None, None, None, None, None, None, None, None]
]

board_hardest = [
    [5, 3, None, None, 7, None, None, None, None],
    [6, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, 3],
    [4, None, None, 8, None, 3, None, None, 1],
    [7, None, None, None, 2, None, None, None, 6],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, 8, None, None, 7, 9]
    ]

to_solve = sudokuBoard(board_hardest)

print(str(to_solve))
if to_solve.solve():
    print(str(to_solve))
else:
    print("Can't be solved")