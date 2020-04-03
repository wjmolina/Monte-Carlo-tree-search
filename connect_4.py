class connect_4(object):
    def __init__(self, board_state=None, action_state=None, whose_turn=1, is_game_over=False, winner=0):
        self.board_state = board_state if board_state is not None else [0] * 42
        self.action_state = action_state if action_state is not None else [5] * 7
        self.whose_turn = whose_turn
        self.is_game_over = is_game_over
        self.winner = winner

    def copy(self):
        return connect_4(self.board_state.copy(), self.action_state.copy(), self.whose_turn, self.is_game_over, self.winner)

    def get_actions(self):
        return [i for i in range(len(self.action_state)) if self.action_state[i] >= 0]

    def get_children(self):
        children = []
        for action in self.get_actions():
            child = self.copy()
            child.play(action)
            children.append(child)
        return children

    def play(self, action):
        self.board_state[self.action_state[action] * 7 + action] = self.whose_turn
        self.whose_turn = 3 - self.whose_turn
        self.action_state[action] -= 1
        self.evaluate()

    def display(self):
        for i in range(6):
            for j in range(7):
                piece = self.board_state[i * 7 + j]
                print('x' if piece == 1 else 'o' if piece == 2 else '.', end = '')
            print()
        print()

    def evaluate(self):
        for i in range(6):
            for j in range(4):
                if 0 != self.board_state[i * 7 + j] == self.board_state[i * 7 + j + 1] == self.board_state[i * 7 + j + 2] == self.board_state[i * 7 + j + 3]:
                    self.is_game_over = True
                    self.winner = self.board_state[i * 7 + j]
                    return
        for i in range(3):
            for j in range(7):
                if 0 != self.board_state[i * 7 + j] == self.board_state[(i + 1) * 7 + j] == self.board_state[(i + 2) * 7 + j] == self.board_state[(i + 3) * 7 + j]:
                    self.is_game_over = True
                    self.winner = self.board_state[i * 7 + j]
                    return
        for i in range(3):
            for j in range(4):
                if 0 != self.board_state[i * 7 + j] == self.board_state[(i + 1) * 7 + j + 1] == self.board_state[(i + 2) * 7 + j + 2] == self.board_state[(i + 3) * 7 + j + 3]:
                    self.is_game_over = True
                    self.winner = self.board_state[i * 7 + j]
                    return
        for i in range(3, 6):
            for j in range(4):
                if 0 != self.board_state[i * 7 + j] == self.board_state[(i - 1) * 7 + j + 1] == self.board_state[(i - 2) * 7 + j + 2] == self.board_state[(i - 3) * 7 + j + 3]:
                    self.is_game_over = True
                    self.winner = self.board_state[i * 7 + j]
                    return
        if self.get_actions() == []:
            self.is_game_over = True
            self.winner = 0