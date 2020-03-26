import keyboard

from math import log, sqrt
from multiprocessing import Pool
from random import choice

class Hexxagon:
    def __init__(self, board=((1, 0, 0, 0, 0, 0, 0, 2), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (2, 0, 0, 0, 0, 0, 0, 1)), turn=1, nmoves=0):
        self._board = board
        self.whose_turn = turn
        self._nmoves = nmoves

    def get_actions(self):
        if self._nmoves >= 100:
            return ()
        pcsLocs = ((i, j) for i in range(8) for j in range(8) if self._board[i][j] == self.whose_turn)
        return tuple(((idx, jdx), (i, j)) for idx, jdx in pcsLocs for i in range(idx - 2, idx + 3) for j in range(jdx - 2, jdx + 3) if 0 <= i < 8 and 0 <= j < 8 and self._board[i][j] == 0)

    def play(self, move):
        if self.is_game_over:
            print('game over: can\'t move')
        elif move not in self.get_actions():
            print('illegal move')
        else:
            board = [list(row) for row in self._board]
            if Hexxagon.ChebyshevDistance(move[0], move[1]) == 1:
                board[move[1][0]][move[1][1]] = self.whose_turn
            else:
                board[move[0][0]][move[0][1]] = 0
                board[move[1][0]][move[1][1]] = self.whose_turn
            for i in range(move[1][0] - 1, move[1][0] + 2):
                for j in range(move[1][1] - 1, move[1][1] + 2):
                    if 0 <= i < 8 and 0 <= j < 8 and self._board[i][j] == 3 - self.whose_turn:
                        board[i][j] = self.whose_turn
            self._board = tuple(tuple(row) for row in board)
            self.whose_turn = 3 - self.whose_turn
            self._nmoves += 1

    def display(self):
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
        if not self.is_game_over:
            return 0
        count1, count2 = self.CountPieces()
        return 1 if count1 > count2 else 2 if count1 < count2 else 0

    def IsGameOver(self):
        return self.get_actions() == ()

    def copy(self):
        return Hexxagon(self._board, self.whose_turn, self._nmoves)

    @staticmethod
    def ChebyshevDistance(x, y):
        return max([abs(x[i] - y[i]) for i in range(len(x))])

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

class MiV_eGG:
    class Node:
        def __init__(self, value, parent=None):
            self._value = value
            self._parent = parent
            self._win = 0
            self._total = 0
            self._children = {}

    def __init__(self, value):
        self._pointer = self.Node(value.copy())

    def Selection(self):
        pointer = self._pointer
        while len(pointer._children) != 0:
            #################
            # Random Search #
            #################
            # pointer = choice(list(pointer._children.values()))

            ################$
            # Clever Search #
            ################$
            tmp = []
            for child in list(pointer._children.values()):
                try:
                    tmp.append([child._win / child._total + sqrt(2) * sqrt(log(child._parent._total) / child._total), child])
                except:
                    return child
            pointer = max(tmp, key=lambda x : x[0])[1]
        return pointer

    def Expansion(self, pointer):
        for move in pointer._value.get_actions():
            child = pointer._value.copy()
            child.play(move)
            pointer._children[move] = self.Node(child, pointer)
        children = list(pointer._children.values())
        return choice(children) if len(children) != 0 else pointer

    def Simulation(self, pointer):
        board = pointer._value.copy()
        while not board.is_game_over:
            board.play(choice(board.get_actions()))
        return board.winner

    def BackPropagation(self, pointer, result):
        while pointer is not None:
            pointer._total += 1
            pointer._win += .5 if result == 0 else 1 if pointer._value.whose_turn == 3 - result else 0
            pointer = pointer._parent

    def Learn(self, times):
        for _ in range(times):
            selection = self.Selection()
            expansion = self.Expansion(selection)
            result = self.Simulation(expansion)
            self.BackPropagation(expansion, result)

    def get_best_move(self):
        return max([[child, move] for move, child in self._pointer._children.items()], key=lambda x: x[0]._win)[1]

    def play(self, move):
        self._pointer = self._pointer._children[move]
        self._pointer._parent = None

class MiV_MiniMaximus:
    def __init__(self, game):
        self._game = game.copy()

    def play(self, move):
        self._game.play(move)

    def get_best_move(self, depth, player):
        return MiV_MiniMaximus.GetBestMoveHelper(self._game, depth, float('-inf'), float('inf'), True, player)[1]

    @staticmethod
    def GetBestMoveHelper(node, depth, alpha, beta, isMaxPlayer, player):
        if depth == 0 or node.is_game_over:
            return [.5 if node.winner == 0 else 1 if node.winner == player else - 1, None]
        if isMaxPlayer:
            value, move = float('-inf'), None
            for move in node.get_actions():
                child = node.copy()
                child.play(move)
                value, move = max([value, move], [MiV_MiniMaximus.GetBestMoveHelper(child, depth - 1, alpha, beta, False, 3 - player)[0], move], key=lambda x: x[0])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, move
        else:
            value, move = float('inf'), None
            for move in node.get_actions():
                child = node.copy()
                child.play(move)
                value, move = min([value, move], [MiV_MiniMaximus.GetBestMoveHelper(child, depth - 1, alpha, beta, True, 3 - player)[0], move], key=lambda x: x[0])
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, move

# def MultiProcessedPlay(agent, count):
#     agent.Learn(count)
#     return agent

# if __name__ == '__main__':
#     toyGame1 = Hexxagon()
#     miV_eGG1, miV_eGG2 = MiV_eGG(toyGame1), MiV_eGG(toyGame1)
#     toyGame1.display()

#     with Pool() as p:
#         while not toyGame1.is_game_over:
#             miV_eGG1, miV_eGG2 = p.starmap(MultiProcessedPlay, [(miV_eGG1, 100), (miV_eGG2, 50)])
#             bestMve1 = miV_eGG1.get_best_move()
#             toyGame1.play(bestMve1)
#             miV_eGG1.play(bestMve1)
#             miV_eGG2.play(bestMve1)
#             toyGame1.display()

#             miV_eGG1, miV_eGG2 = p.starmap(MultiProcessedPlay, [(miV_eGG1, 100), (miV_eGG2, 50)])
#             bestMve2 = miV_eGG2.get_best_move()
#             toyGame1.play(bestMve2)
#             miV_eGG1.play(bestMve2)
#             miV_eGG2.play(bestMve2)
#             toyGame1.display()

toyGame = connect_4(board_state=[0,0,0,1,0,0,0,
                                 0,0,1,2,2,0,0,
                                 0,0,2,2,1,0,0,
                                 0,0,1,1,2,0,0,
                                 0,0,2,2,1,2,1,
                                 0,0,2,1,2,1,1,], action_state=[5, 5, 0, - 1, 0, 3, 3], whose_turn=1, is_game_over=False, winner=0)
miV_eGG = MiV_eGG(toyGame)
toyGame.display()
while not toyGame.is_game_over:
    # cnt = 0
    # while True:
    #     if keyboard.is_pressed('q'):
    #         print('done learning')
    #         break
    #     miV_eGG.Learn(1000)
    #     cnt += 1
    #     print(cnt, 'learning')
    # print('ENTER TO PROCEED')
    # input()
    miV_eGG.Learn(200000)
    bestMove = miV_eGG.get_best_move()
    toyGame.play(bestMove)
    miV_eGG.play(bestMove)
    toyGame.display()
    if toyGame.is_game_over:
        break
    # cnt = 0
    # while True:
    #     if keyboard.is_pressed('q'):
    #         print('done learning')
    #         break
    #     miV_eGG.Learn(1000)
    #     cnt += 1
    #     print(cnt, 'learning')
    # print('ENTER TO PROCEED')
    # input()
    miV_eGG.Learn(200000)
    print('your move')
    bestMove = int(input())
    toyGame.play(bestMove)
    miV_eGG.play(bestMove)
    toyGame.display()