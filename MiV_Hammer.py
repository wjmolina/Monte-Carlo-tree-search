from hexgame2 import hexgame2
from random import choice

class MiV_Hammer:
    def __init__(self, game):
        self._game = game.copy()

    def play(self, move):
        self._game.play(move)

    def get_best_move(self, depth, isMaxPlayer):
        result = MiV_Hammer.get_best_move_helper(self._game, depth, float('-inf'), float('inf'), isMaxPlayer)
        print(result[0])
        return result[1]

    @staticmethod
    def get_best_move_helper(node, depth, alpha, beta, isMaxPlayer):
        if depth == 0 or node.is_game_over:
            return [node.heuristic(), None]
        if isMaxPlayer:
            value, move = float('-inf'), None
            for move in node.get_actions():
                child = node.copy()
                child.play(move)
                value, move = max([value, move], [MiV_Hammer.get_best_move_helper(child, depth - 1, alpha, beta, False)[0], move], key=lambda x: x[0])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, move
        else:
            value, move = float('inf'), None
            for move in node.get_actions():
                child = node.copy()
                child.play(move)
                value, move = min([value, move], [MiV_Hammer.get_best_move_helper(child, depth - 1, alpha, beta, True)[0], move], key=lambda x: x[0])
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, move

game = hexgame2(4, 4)
hammer = MiV_Hammer(game)
game.display()
while not game.is_game_over:
    random_move = choice(game.get_actions())
    hammer.play(random_move)
    game.play(random_move)
    game.display()
    if game.is_game_over:
        break
    hammer_move = hammer.get_best_move(8, False)
    hammer.play(hammer_move)
    game.play(hammer_move)
    game.display()
print(game.winner)