class Board:
    def __init__(self, board_size):
        self.size = board_size
        self.board = [' ' for _ in range(board_size * board_size)]

    def getRawBoard(self):
        return self.board

    def play(self, player, x, y):
        if self.board[y * self.size + x] != ' ':
            return False
        self.board[y * self.size + x] = player
        return True

    def getNbMaxAligned(self, player):
        max = 0
        for y in range(self.size):
            for x in range(self.size):
                value = self._checkVertical(player, x, y)
                if value > max:
                    max = value
                value = self._checkHorizontal(player, x, y)
                if value > max:
                    max = value
                value = self._checkDiagonalLeft(player, x, y)
                if value > max:
                    max = value
                value = self._checkDiagonalRight(player, x, y)
                if value > max:
                    max = value
                if max >= 5:
                    break
        return max

    def isFull(self):
        for it in self.board:
            if it == ' ':
                return False
        return True

    def _checkVertical(self, player, x, y):
        out = 0.
        for i in range(5):
            if y + i >= self.size:
                break
            current = self.board[(y + i) * self.size + x]
            if current == player:
                out += 1
            elif current != ' ':
                break
        return out

    def _checkHorizontal(self, player, x, y):
        out = 0.
        for i in range(5):
            if x + i >= self.size:
                break
            current = self.board[y * self.size + x + i]
            if current == player:
                out += 1
            elif current != ' ':
                break
        return out

    def _checkDiagonalLeft(self, player, x, y):
        out = 0.
        for i in range(5):
            if x - i < 0 or y + i >= self.size:
                break
            current = self.board[(y + i) * self.size + x - i]
            if current == player:
                out += 1
            elif current != ' ':
                break
        return out

    def _checkDiagonalRight(self, player, x, y):
        out = 0.
        for i in range(5):
            if x + i >= self.size or y + i >= self.size:
                break
            current = self.board[(y + i) * self.size + x + i]
            if current == player:
                out += 1
            elif current != ' ':
                break
        return out

if __name__ == "__main__":
    b = Board(20)
    print(b.getNbMaxAligned('O'))
