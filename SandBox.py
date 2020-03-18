from math import log, sqrt
from random import choice

class SandBox:
    def __init__(self, board=((1, 0, 0, 0, 0, 0, 0, 2), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (2, 0, 0, 0, 0, 0, 0, 1)), turn=1, nmoves=0):
        self._board = board
        self._turn = turn
        self._nmoves = nmoves

    def GetMoves(self):
        if self._nmoves >= 100:
            return ()
        pcsLocs = ((i, j) for i in range(8) for j in range(8) if self._board[i][j] == self._turn)
        return tuple(((idx, jdx), (i, j)) for idx, jdx in pcsLocs for i in range(idx - 2, idx + 3) for j in range(jdx - 2, jdx + 3) if 0 <= i < 8 and 0 <= j < 8 and self._board[i][j] == 0)

    def MakeMove(self, move):
        if self.IsGameOver():
            print('game over: cannot move')
        elif move not in self.GetMoves():
            print('illegal move')
        else:
            board = [list(row) for row in self._board]
            if self.ChebyshevDistance(move[0], move[1]) == 1:
                board[move[1][0]][move[1][1]] = self._turn
            else:
                board[move[0][0]][move[0][1]] = 0
                board[move[1][0]][move[1][1]] = self._turn
            for i in range(move[1][0] - 1, move[1][0] + 2):
                for j in range(move[1][1] - 1, move[1][1] + 2):
                    if 0 <= i < 8 and 0 <= j < 8 and self._board[i][j] == 3 - self._turn:
                        board[i][j] = self._turn
            self._board = tuple(tuple(row) for row in board)
            self._turn = 3 - self._turn
            self._nmoves += 1

    def Display(self):
        for i in range(8):
            for j in range(8):
                print('x' if self._board[i][j] == 1 else 'o' if self._board[i][j] == 2 else '.', end='')
            print()
        print(self._nmoves)
        print(*self.CountPieces())

    def CountPieces(self):
        count1, count2 = 0, 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == 1:
                    count1 += 1
                elif self._board[i][j] == 2:
                    count2 += 1
        return count1, count2

    def GetWinner(self):
        if not self.IsGameOver():
            return 0
        count1, count2 = self.CountPieces()
        return 1 if count1 > count2 else 2 if count1 < count2 else 0

    def IsGameOver(self):
        return self.GetMoves() == ()

    def Copy(self):
        return SandBox(self._board, self._turn, self._nmoves)

    @staticmethod
    def ChebyshevDistance(x, y):
        return max([abs(x[i] - y[i]) for i in range(len(x))])

class Node:
    def __init__(self, value, parent=None):
        self._value = value
        self._parent = parent
        self._win = 0
        self._total = 0
        self._children = {}

class MiV_eGG:
    def __init__(self, value):
        self._pointer = Node(value.Copy())

    def Selection(self):
        pointer = self._pointer
        while len(pointer._children) != 0:
            # pointer = choice(list(pointer._children.values()))
            pointer = max([[(child._win + 1) / (child._total + 1) + sqrt(4 * log((child._parent._total + 1)) / (child._total + 1)), child] for child in list(pointer._children.values())], key=lambda x : x[0])[1]
        return pointer

    def Expansion(self, pointer):
        for move in pointer._value.GetMoves():
            child = pointer._value.Copy()
            child.MakeMove(move)
            pointer._children[move] = Node(child, pointer)
        children = list(pointer._children.values())
        return choice(children) if len(children) != 0 else pointer

    def Simulation(self, pointer):
        board = pointer._value.Copy()
        while not board.IsGameOver():
            board.MakeMove(choice(board.GetMoves()))
        return board.GetWinner()

    def BackPropagation(self, pointer, result):
        while pointer is not None:
            pointer._total += 1
            pointer._win += .5 if result == 0 else 1 if pointer._value._turn == 3 - result else 0
            pointer = pointer._parent

    def Learn(self, times):
        for _ in range(times):
            selection = self.Selection()
            expansion = self.Expansion(selection)
            result = self.Simulation(expansion)
            self.BackPropagation(expansion, result)

    def GetBestMove(self):
        return max([[child, move] for move, child in self._pointer._children.items()], key=lambda x: x[0]._win)[1]

    def MakeMove(self, move):
        self._pointer = self._pointer._children[move]
        self._pointer._parent = None

toy = [[0 for _ in range(8)] for _ in range(8)]
toy[3][3] = 1
toy[2][5] = 2
toy[2][6] = 2
toy[3][5] = 2
toy[3][6] = 2
toy[4][6] = 2
toy[5][5] = 2
toy[5][6] = 2
toy = tuple(tuple(row) for row in toy)

sandBox = SandBox(toy)
miV_eGG = MiV_eGG(sandBox)
sandBox.Display()
while not sandBox.IsGameOver():
    miV_eGG.Learn(5000)
    bestMove = miV_eGG.GetBestMove()
    miV_eGG.MakeMove(bestMove)
    sandBox.MakeMove(bestMove)
    sandBox.Display()
    print()
    if sandBox.IsGameOver():
        break
    miV_eGG.Learn(5000)
    bestMove = miV_eGG.GetBestMove()
    miV_eGG.MakeMove(bestMove)
    sandBox.MakeMove(bestMove)
    sandBox.Display()
    print()