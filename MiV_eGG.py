from math import log, sqrt
from multiprocessing import Pool
from random import choice

class ToyGame:
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
            print('game over: can\'t move')
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
        return ToyGame(self._board, self._turn, self._nmoves)

    @staticmethod
    def ChebyshevDistance(x, y):
        return max([abs(x[i] - y[i]) for i in range(len(x))])

class MiV_eGG:
    class Node:
        def __init__(self, value, parent=None):
            self._value = value
            self._parent = parent
            self._win = 0
            self._total = 0
            self._children = {}

    def __init__(self, value):
        self._pointer = self.Node(value.Copy())

    def Selection(self):
        pointer = self._pointer
        while len(pointer._children) != 0:
            # pointer = choice(list(pointer._children.values())) # Random Search
            pointer = max([[child._win / (child._total + 1) + sqrt(4 * log(child._parent._total) / (child._total + 1)), child] for child in list(pointer._children.values())], key=lambda x : x[0])[1] # Smart Search
        return pointer

    def Expansion(self, pointer):
        for move in pointer._value.GetMoves():
            child = pointer._value.Copy()
            child.MakeMove(move)
            pointer._children[move] = self.Node(child, pointer)
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

class MiV_Hammer:
    def __init__(self, game):
        self._game = game.Copy()

    def MakeMove(self, move):
        self._game.MakeMove(move)

    def GetBestMove(self, depth, player):
        return MiV_Hammer.GetBestMoveHelper(self._game, depth, float('-inf'), float('inf'), True, player)[1]

    @staticmethod
    def GetBestMoveHelper(node, depth, alpha, beta, isMaxPlayer, player):
        if depth == 0 or node.IsGameOver():
            return [.5 if node.GetWinner() == 0 else 1 if node.GetWinner() == player else - 1, None]
        if isMaxPlayer:
            value, move = float('-inf'), None
            for move in node.GetMoves():
                child = node.Copy()
                child.MakeMove(move)
                value, move = max([value, None], [MiV_Hammer.GetBestMoveHelper(child, depth - 1, alpha, beta, False, 3 - player), move], key=lambda x: x[0])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, move
        else:
            value, move = float('inf'), None
            for move in node.GetMoves():
                child = node.Copy()
                child.MakeMove(move)
                value, move = min([value, None], [MiV_Hammer.GetBestMoveHelper(child, depth - 1, alpha, beta, True, 3 - player), move], key=lambda x: x[0])
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, move

# def MultiProcessedPlay(agent, count):
#     agent.Learn(count)
#     return agent

# if __name__ == '__main__':
#     toyGame1 = ToyGame()
#     miV_eGG1, miV_eGG2 = MiV_eGG(toyGame1), MiV_eGG(toyGame1)
#     toyGame1.Display()

#     with Pool() as p:
#         while not toyGame1.IsGameOver():
#             miV_eGG1, miV_eGG2 = p.starmap(MultiProcessedPlay, [(miV_eGG1, 100), (miV_eGG2, 50)])
#             bestMve1 = miV_eGG1.GetBestMove()
#             toyGame1.MakeMove(bestMve1)
#             miV_eGG1.MakeMove(bestMve1)
#             miV_eGG2.MakeMove(bestMve1)
#             toyGame1.Display()

#             miV_eGG1, miV_eGG2 = p.starmap(MultiProcessedPlay, [(miV_eGG1, 100), (miV_eGG2, 50)])
#             bestMve2 = miV_eGG2.GetBestMove()
#             toyGame1.MakeMove(bestMve2)
#             miV_eGG1.MakeMove(bestMve2)
#             miV_eGG2.MakeMove(bestMve2)
#             toyGame1.Display()

toyGame = ToyGame()
miV_eGG = MiV_eGG(toyGame)
miV_Hammer = MiV_Hammer(toyGame)
toyGame.Display()

while not toyGame.IsGameOver():
    miV_eGG.Learn(100)
    bestMove = miV_eGG.GetBestMove()
    toyGame.MakeMove(bestMove)
    miV_eGG.MakeMove(bestMove)
    miV_Hammer.MakeMove(bestMove)
    toyGame.Display()

    if toyGame.IsGameOver():
        break

    bestMove = miV_Hammer.GetBestMove(4, 2)
    toyGame.MakeMove(bestMove)
    miV_eGG.MakeMove(bestMove)
    miV_Hammer.MakeMove(bestMove)
    toyGame.Display()
