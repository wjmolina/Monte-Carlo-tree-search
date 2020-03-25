class n_in_a_row:
    def __init__(self, rows=5, columns=5, number_in_a_row=4, boardState=(0,) * 25, whose_turn=1, is_game_over=False, winner=0):
        self.rows = rows
        self.columns = columns
        self.number_in_a_row = number_in_a_row
        self.boardState = boardState
        self.whose_turn = whose_turn
        self.is_game_over = is_game_over
        self.winner = winner
    def copy(self):
        return n_in_a_row(self.rows, self.columns, self.number_in_a_row, self.boardState, self.whose_turn, self.is_game_over, self.winner)
    def get_board_state(self):
        return self.boardState
    def get_actions(self):
        return [] if self.is_game_over else [(i // self.columns, i % self.columns) for i in range(self.rows * self.columns) if self.boardState[i] == 0]
    def get_children(self):
        children = []
        for action in self.get_actions():
            child = self.copy()
            child.play(action)
            children.append(child)
        return children
    def play(self, action):
        if self.boardState[action[0] * self.columns + action[1]] or self.is_game_over:
            print('invalid action')
        else:
            helper = list(self.boardState)
            helper[action[0] * self.columns + action[1]] = self.whose_turn
            self.boardState = tuple(helper)
            self.whose_turn = 3 - self.whose_turn
            self.evaluate()
    def display(self):
        for row in range(self.rows):
            for column in range(self.columns):
                print(' x ' if self.boardState[row * self.columns + column] == 1 else ' o ' if self.boardState[row * self.columns + column] == 2 else ' . ', end = '')
            print()
        print()
    def evaluate(self):
        for row in range(self.rows):
            for column in range(self.columns - self.number_in_a_row + 1):
                if self.boardState[row * self.columns + column] != 0 and all([self.boardState[row * self.columns + (column + cnt)] == self.boardState[row * self.columns + (column + cnt + 1)] for cnt in range(self.number_in_a_row - 1)]):
                    self.is_game_over = True
                    self.winner = self.boardState[row * self.columns + column]
                    return
        for row in range(self.rows - self.number_in_a_row + 1):
            for column in range(self.columns):
                if self.boardState[row * self.columns + column] != 0 and all([self.boardState[(row + cnt) * self.columns + column] == self.boardState[(row + cnt + 1) * self.columns + column] for cnt in range(self.number_in_a_row - 1)]):
                    self.is_game_over = True
                    self.winner = self.boardState[row * self.columns + column]
                    return
        for row in range(self.rows - self.number_in_a_row + 1):
            for column in range(self.columns - self.number_in_a_row + 1):
                if self.boardState[row * self.columns + column] != 0 and all([self.boardState[(row + cnt) * self.columns + (column + cnt)] == self.boardState[(row + cnt + 1) * self.columns + (column + cnt + 1)] for cnt in range(self.number_in_a_row - 1)]):
                    self.is_game_over = True
                    self.winner = self.boardState[row * self.columns + column]
                    return
        for row in range(self.rows - self.number_in_a_row + 1):
            for column in range(self.number_in_a_row - 1, self.columns):
                if self.boardState[row * self.columns + column] != 0 and all([self.boardState[(row + cnt) * self.columns + (column - cnt)] == self.boardState[(row + cnt + 1) * self.columns + (column - cnt - 1)] for cnt in range(self.number_in_a_row - 1)]):
                    self.is_game_over = True
                    self.winner = self.boardState[row * self.columns + column]
                    return
        if 0 not in self.boardState:
            self.is_game_over = True
            self.winner = 0
            return
        self.is_game_over = False
        self.winner = 0