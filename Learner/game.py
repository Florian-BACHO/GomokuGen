BOARD_SIZE = 20

def getEmptyBoard():
    out = []
    for _ in range(BOARD_SIZE):
        tmp = []
        for _2 in range(BOARD_SIZE):
            tmp.append(' ')
        out.append(tmp)
    return out

def possible_moves(board):
    out = []
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == ' ':
                out.append(y * BOARD_SIZE + x)
    return out

def _checkVertical(board, player, x, y):
    out = 0.
    for i in range(5):
        if y + i >= BOARD_SIZE:
            break
        current = board[y + i][x]
        if current == player:
            out += 1
        else:
            break
    return out

def _checkHorizontal(board, player, x, y):
    out = 0.
    for i in range(5):
        if x + i >= BOARD_SIZE:
            break
        current = board[y][x + i]
        if current == player:
            out += 1
        else:
            break
    return out

def _checkDiagonalLeft(board, player, x, y):
    out = 0.
    for i in range(5):
        if x - i < 0 or y + i >= BOARD_SIZE:
            break
        current = board[y + i][x - i]
        if current == player:
            out += 1
        else:
            break
    return out

def _checkDiagonalRight(board, player, x, y):
    out = 0.
    for i in range(5):
        if x + i >= BOARD_SIZE or y + i >= BOARD_SIZE:
            break
        current = board[y + i][x + i]
        if current == player:
            out += 1
        else:
            break
    return out

def _won(board, player):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if _checkVertical(board, player, x, y) >= 5 or \
               _checkHorizontal(board, player, x, y) >= 5 or \
               _checkDiagonalLeft(board, player, x, y) >= 5 or \
               _checkDiagonalRight(board, player, x, y) >= 5:
                return True
    return False

def move(board, action, player):
    board[action // BOARD_SIZE][action % BOARD_SIZE] = player
    won = _won(board, player)
    return board, won

def render(board):
    tirets = "".join(['-' for _ in range(BOARD_SIZE + 2)]) + "\n"
    out = tirets
    for y, row in enumerate(board):
        out += '|' + "".join(row) + "|\n"
    out += tirets
    return out
