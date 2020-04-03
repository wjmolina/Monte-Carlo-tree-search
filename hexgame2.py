from copy import deepcopy

class hexgame2:
    check = ((- 1, 0), (1, 0), (0, - 1), (0, 1), (- 1, 1), (1, - 1))

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.graph_dict = {(i, j): {'p': 0, 'n': set()} for i in range(rows) for j in range(cols)}
        self.is_game_over = False
        self.whose_turn = 1
        self.winner = 0
        for i in range(rows):
            for j in range(cols):
                for _i, _j in self.check:
                    if (i + _i, j + _j) in self.graph_dict:
                        self.graph_dict[(i, j)]['n'].add((i + _i, j + _j))
        self.graph_dict['1a'] = {'p': 1, 'n': set()}
        for j in range(cols):
            self.graph_dict['1a']['n'].add((0, j))
            self.graph_dict[(0, j)]['n'].add('1a')
        self.graph_dict['1b'] = {'p': 1, 'n': set()}
        for j in range(cols):
            self.graph_dict['1b']['n'].add((rows - 1, j))
            self.graph_dict[(rows - 1, j)]['n'].add('1b')
        self.graph_dict['2a'] = {'p': 2, 'n': set()}
        for i in range(rows):
            self.graph_dict['2a']['n'].add((i, 0))
            self.graph_dict[(i, 0)]['n'].add('2a')
        self.graph_dict['2b'] = {'p': 2, 'n': set()}
        for i in range(rows):
            self.graph_dict['2b']['n'].add((i, cols - 1))
            self.graph_dict[(i, cols - 1)]['n'].add('2b')

    def heuristic(self):
        return float('inf') if self.dijkstra('1a', '1b') == 0 else float('-inf') if self.dijkstra('2a', '2b') == 0 else self.dijkstra('2a', '2b') - self.dijkstra('1a', '1b')

    def play(self, action):
        self.graph_dict[action]['p'] = self.whose_turn
        self.whose_turn = 3 - self.whose_turn
        self.evaluate()

    def evaluate(self):
        if self.dijkstra('1a', '1b') == 0:
            self.is_game_over = True
            self.winner = 1
        elif self.dijkstra('2a', '2b') == 0:
            self.is_game_over = True
            self.winner = 2

    def display(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print('x' if self.graph_dict[(i, j)]['p'] == 1 else 'o' if self.graph_dict[(i, j)]['p'] == 2 else '.', end='')
            print()
        print()

    def get_actions(self):
        actions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.graph_dict[(i, j)]['p'] == 0:
                    actions.append((i, j))
        return actions

    def copy(self):
        return deepcopy(self)

    def length(self, a, b, p):
        S = set([self.graph_dict[a]['p'], self.graph_dict[b]['p']])
        if 0 in S and len(S) == 1 or 0 in S and p in S:
            return 1
        if 0 in S and 3 - p in S or p in S and 3 - p in S or 3 - p in S and len(S) == 1:
            return float('inf')
        return 0

    def dijkstra(self, source, target):
        Q = set()
        dist = {}
        for v in self.graph_dict:
            dist[v] = float('inf')
            Q.add(v)
        dist[source] = 0
        while Q != set():
            u = min(Q, key=lambda v: dist[v])
            Q.remove(u)
            if u == target:
                return dist[target]
            for v in self.graph_dict[u]['n'] & Q:
                alt = dist[u] + self.length(u, v, self.graph_dict[source]['p'])
                if alt < dist[v]:
                    dist[v] = alt
        return dist[target]
