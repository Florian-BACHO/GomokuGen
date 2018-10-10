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

    def step(self, currentPlayer, advers, action):
        y = int(action / self.size)
        x = int(action) % self.size
        rewardCurrent = 0.
        rewardAdvers = 0.
        done = False

        playResult = self.board.play(currentPlayer, x, y)
        nbMaxAlignedCurrent = self.board.getNbMaxAligned(currentPlayer)

        if playResult == False or nbMaxAlignedCurrent >= 5 or \
           self.board.isFull():
            rewardCurrent = nbMaxAlignedCurrent
            rewardAdvers = self.board.getNbMaxAligned(advers)
            done = True

        obs = self.board.getRawBoard()

        return self._rawBoardToBatch(obs), rewardCurrent, rewardAdvers, done

    def render(self):
        raw = self.board.getRawBoard()
        print("".join(['-' for _ in range(self.size + 2)]))
        for y in range(self.size):
            print("|" + "".join([raw[y * self.size + x] for x in range(self.size)]) + "|")
        print("".join(['-' for _ in range(self.size + 2)]))
        print()
