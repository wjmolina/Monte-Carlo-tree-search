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