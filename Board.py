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

    def playerHaveWin(self, player):
        for y in range(self.size):
            for x in range(self.size):
                if self._checkVertical(player, x, y) or \
                   self._checkHorizontal(player, x, y) or \
                   self._checkDiagonalLeft(player, x, y) or \
                   self._checkDiagonalRight(player, x, y):
                    return True
        return False

    def isFull(self):
        for it in self.board:
            if it == ' ':
                return False
        return True

    def _checkVertical(self, player, x, y):
        if y > self.size - 5:
            return False
        for i in range(5):
            if self.board[(y + i) * self.size + x] != player:
                return False
        return True

    def _checkHorizontal(self, player, x, y):
        if x > self.size - 5:
            return False
        for i in range(5):
            if self.board[y * self.size + x + i] != player:
                return False
        return True

    def _checkDiagonalLeft(self, player, x, y):
        if x < 4 or y > self.size - 5:
            return False
        for i in range(5):
            if self.board[(y + i) * self.size + x - i] != player:
                return False
        return True

    def _checkDiagonalRight(self, player, x, y):
        if x > self.size - 5 or y > self.size - 5:
            return False
        for i in range(5):
            if self.board[(y + i) * self.size + x + i] != player:
                return False
        return True
