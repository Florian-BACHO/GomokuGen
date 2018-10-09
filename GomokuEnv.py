from Board import *

class GomokuEnv:
    def __init__(self, board_size=20):
        self.size = board_size
        self.reset()

    def reset(self):
        self.board = Board(self.size)
        return self._rawBoardToBatch(self.board.getRawBoard())

    def _rawBoardToBatch(self, raw):
        out = []

        for it in raw:
            if it == ' ':
                out.append(0.)
            elif it == 'O':
                out.append(1.)
            elif it == 'X':
                out.append(-1.)
            else:
                raise ValueError("Invalid character")

        return out

    def step(self, player, action):
        y = int(action / self.size)
        x = int(action) % self.size
        reward = 0.
        done = False

        if self.board.play(player, x, y) == False:
            reward = -1.
            done = True
        elif self.board.playerHaveWin(player):
            reward = 1.
            done = True
        elif self.board.isFull():
            reward = 0.
            done = True

        obs = self.board.getRawBoard()

        return self._rawBoardToBatch(obs), reward, done

    def render(self):
        raw = self.board.getRawBoard()
        print("".join(['-' for _ in range(self.size + 2)]))
        for y in range(self.size):
            print("|" + "".join([raw[y * self.size + x] for x in range(self.size)]) + "|")
        print("".join(['-' for _ in range(self.size + 2)]))
        print()
