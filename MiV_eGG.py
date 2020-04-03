import keyboard

from math import log, sqrt
from multiprocessing import Pool
from random import choice, random
from hex_game import hex_game

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

            #################
            # Epsilon Greed #
            #################
            # UNTESTED
            # pointer = choice(list(pointer._children.values())) if random() < .1 else max([[child, child._win / (child._total + 1)] for child in pointer._children.values()], key=lambda x: x[1])[0]

            ################$
            # Clever Search #
            ################$
            tmp = []
            for child in list(pointer._children.values()):
                try:
                    tmp.append([child._win / child._total + sqrt(log(child._parent._total + 1) / child._total), child])
                except:
                    return child
            pointer = max(tmp, key=lambda x: x[0])[1]
            
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
            board.play_sim(choice(tuple(board.get_actions())))
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

# game = hex_game()
# miV_eGG = MiV_eGG(game)
# game.display()
# while not game.is_game_over:
#     # cnt = 0
#     # while True:
#     #     if keyboard.is_pressed('q'):
#     #         print('done learning')
#     #         break
#     #     miV_eGG.Learn(1000)
#     #     cnt += 1
#     #     print(cnt, 'learning')
#     # print('ENTER TO PROCEED')
#     # input()
#     miV_eGG.Learn(250000)
#     bestMove = miV_eGG.get_best_move()
#     game.play(bestMove)
#     miV_eGG.play(bestMove)
#     game.display()
#     if game.is_game_over:
#         break
#     # cnt = 0
#     # while True:
#     #     if keyboard.is_pressed('q'):
#     #         print('done learning')
#     #         break
#     #     miV_eGG.Learn(1000)
#     #     cnt += 1
#     #     print(cnt, 'learning')
#     # print('ENTER TO PROCEED')
#     # input()
#     miV_eGG.Learn(250000)
#     print('your move')
#     bestMove = int(input())
#     game.play(bestMove)
#     miV_eGG.play(bestMove)
#     game.display()

game = hex_game(8, 8)
eGG1 = MiV_eGG(game)
game.display()
while not game.is_game_over:
    eGG1.Learn(100000)
    eGG1_move = eGG1.get_best_move()
    game.play(eGG1_move)
    eGG1.play(eGG1_move)
    game.display()
print(game.winner)