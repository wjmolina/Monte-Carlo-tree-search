from copy import deepcopy

class hex_game:
    checks = ((- 1, 0), (1, 0), (0, 1), (0, - 1), (- 1, 1), (1, - 1))

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.game_state = [[0 for _ in range(columns)] for _ in range(rows)]
        self.whose_turn = 1
        self.is_game_over = False
        self.valid_actions = set((i, j) for i in range(rows) for j in range(columns))

    def copy(self):
        return deepcopy(self)

    def get_actions(self):
        return self.valid_actions

    def evaluate(self):
        g1, g2 = self.get_graph(1), self.get_graph(2)
        if self.are_connected(g1, 'a', 'b'):
            self.is_game_over = True
            self.winner = 1
        elif self.are_connected(g2, 'a', 'b'):
            self.is_game_over = True
            self.winner = 2

    def play(self, action):
        self.play_sim(action)
        self.evaluate()

    def play_sim(self, action):
        if action in self.valid_actions:
            self.game_state[action[0]][action[1]] = self.whose_turn
            self.whose_turn = 3 - self.whose_turn
            self.valid_actions.remove(action)
            if self.valid_actions == set():
                self.evaluate()
        else:
            print('invalid move')

    def get_graph(self, player):
        graph = {}
        for i in range(self.rows):
            for j in range(self.columns):
                if self.game_state[i][j] == player:
                    graph[(i, j)] = set()
                    for ii, jj in self.checks:
                        if 0 <= i + ii < self.rows and 0 <= j + jj < self.columns and self.game_state[i + ii][j + jj] == player:
                            graph[(i, j)].add((i + ii, j + jj))
        graph['a'], graph['b'] = set(), set()
        for i in range(self.columns if player == 1 else self.rows):
            I, J = (0, i) if player == 1 else (i, 0)
            if self.game_state[I][J] == player:
                graph['a'].add((I, J))
                graph[(I, J)].add('a')
            I, J = (self.rows - 1, i) if player == 1 else (i, self.columns - 1)
            if self.game_state[I][J] == player:
                graph['b'].add((I, J))
                graph[(I, J)].add('b')
        return graph

    def are_connected(self, graph, a, b):
        P, Q = set(), set([a])
        while Q != set():
            Qn = set()
            for u in Q:
                P.add(u)
                if u == b:
                    return True
                for v in graph[u]:
                    if v not in P:
                        Qn.add(v)
            Q = Qn
        return False

    def display(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print('x' if self.game_state[i][j] == 1 else 'o' if self.game_state[i][j] == 2 else '.', end = '')
            print()
        print()
