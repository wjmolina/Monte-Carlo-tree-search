from random import choice

class hexgame:
    def __init__(self, state=(), whose_turn=1, is_game_over=False, rows=6, cols=6):
        self.state = state
        self.whose_turn = whose_turn
        self.is_game_over = is_game_over
        self.rows = rows
        self.cols = cols
        self.winner = 0
    def get_neighbors(self, hexagon):
        neighbors = []
        checks = ((- 1, 0), (1, 0), (0, - 1), (0, 1), (- 1, 1), (1, - 1))
        for check in checks:
            neighbor = (hexagon[0], hexagon[1] + check[0], hexagon[2] + check[1])
            if neighbor in self.state:
                neighbors.append(neighbor)
        return tuple(neighbors)
    def copy(self):
        return hexgame(self.state, self.whose_turn, self.is_game_over, self.rows, self.cols)
    def get_children(self):
        children = []
        for action in self.get_actions():
            child = self.copy()
            child.play(action)
            children.append(child)
        return children
    def play(self, move):
        self.state = list(self.state)
        self.state.append((self.whose_turn,) + move)
        self.whose_turn = 3 - self.whose_turn
        self.evaluate()
    def are_connected(self, start_hexagon, end_hexagon):
        p, q = set(), set([start_hexagon])
        while q != set():
            qn = set()
            for n in q:
                p.add(n)
                if n == end_hexagon:
                    return True
                for m in self.get_neighbors(n):
                    if m not in p:
                        qn.add(m)
            q = qn
        return False
    def get_actions(self):
        moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if (1, i, j) not in self.state and (2, i, j) not in self.state:
                    moves.append((i, j))
        return tuple(moves)
    def display(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print('x' if (1, i, j) in self.state else 'o' if (2, i, j) in self.state else '.', end='')
            print()
        print()
    def evaluate(self):
        for i in range(self.cols):
            for j in range(self.cols):
                if (1, 0, i) in self.state and (1, self.rows - 1, j) in self.state and self.are_connected((1, 0, i), (1, self.rows - 1, j)):
                    self.is_game_over = True
                    self.winner = 1
        for i in range(self.rows):
            for j in range(self.rows):
                if (2, i, 0) in self.state and (2, j, self.cols - 1) in self.state and self.are_connected((2, i, 0), (2, j, self.cols - 1)):
                    self.is_game_over = True
                    self.winner = 2
