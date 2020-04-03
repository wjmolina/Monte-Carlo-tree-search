class connect_4_binary(object):
    wcs = set([4123168604160, 2061584302080, 1030792151040, 515396075520, 32212254720, 16106127360, 8053063680, 4026531840, 251658240, 125829120, 62914560, 31457280, 1966080, 983040, 491520, 245760, 15360, 7680, 3840, 1920, 120, 60, 30, 15, 2216338391040, 1108169195520, 554084597760, 277042298880, 138521149440, 69260574720, 34630287360, 17315143680, 8657571840, 4328785920, 2164392960, 1082196480, 541098240, 270549120, 135274560, 67637280, 33818640, 16909320, 8454660, 4227330, 2113665, 2207646875648, 1103823437824, 551911718912, 275955859456, 17247241216, 8623620608, 4311810304, 2155905152, 134744072, 67372036, 33686018, 16843009, 279241031680, 139620515840, 69810257920, 34905128960, 2181570560, 1090785280, 545392640, 272696320, 17043520, 8521760, 4260880, 2130440])

    def __init__(self, one=0, two=0, action_state=None, whose_turn=1, is_game_over=False, winner=0):
        self.one = one
        self.two = two
        self.action_state = action_state if action_state is not None else [2 ** (6 - i) for i in range(7)]
        self.whose_turn = whose_turn
        self.is_game_over = is_game_over
        self.winner = winner

    def copy(self):
        return connect_4_binary(self.one, self.two, self.action_state.copy(), self.whose_turn, self.is_game_over, self.winner)

    def get_actions(self):
        return [i for i in range(len(self.action_state)) if self.action_state[i] < 4398046511104]

    def get_children(self):
        children = []
        for action in self.get_actions():
            child = self.copy()
            child.play(action)
            children.append(child)
        return children

    def play(self, action):
        if self.whose_turn == 1:
            self.one += self.action_state[action]
        else:
            self.two += self.action_state[action]
        self.whose_turn = 3 - self.whose_turn
        self.action_state[action] <<= 7
        self.evaluate()

    def display(self):
        data = []
        one = self.one
        two = self.two
        for _ in range(42):
            data.insert(0, 'x' if one % 2 == 1 else 'o' if two % 2 == 1 else '.')
            one >>= 1
            two >>= 1
        cnt = 0
        for _ in range(6):
            for _ in range(7):
                print(data[cnt], end='')
                cnt += 1
            print()
        print()

    def evaluate(self):
        if self.wcs.intersection([p & wc for p in [self.one, self.two] for wc in self.wcs]) != set():
            self.is_game_over = True
            self.winner = 3 - self.whose_turn
        elif self.one + self.two == 4398046511103:
            self.is_game_over = True