"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    NumX = 0
    Num0 = 0
    for i in board:
        for j in i:
            if j == X:
                NumX += 1
            if j == O:
                Num0 += 1
    if NumX <= Num0:
        return X
    else:
        return O


def actions(board):
    possibles = set()
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j] == EMPTY:
                possibles.add((i, j))
    return possibles


def result(board, action):
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("invalid action")
    if len(action) != 2:
        raise Exception("invalid action length")
    else:
        i = action[0]
        j = action[1]
        copyboard = copy.deepcopy(board)
        if copyboard[i][j] == EMPTY:
            copyboard[i][j] = player(board)
            return copyboard
        else:
            raise Exception("invalid action: already done")


def winner(board):
    for i in range(0, 3):
        if board[i][0] != EMPTY and (board[i][0] == board[i][1] == board[i][2]):
            return board[i][2]
        if board[0][i] != EMPTY and (board[0][i] == board[1][i] == board[2][i]):
            return board[2][i]
    if board[0][0] != EMPTY and (board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]
    if board[0][2] != EMPTY and (board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]
    return None

def terminal(board):
    if winner(board) == X or winner(board) == O:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

def minimise(board):
    if terminal(board):
        return utility(board)
    else:
        maxv = math.inf
        for i in actions(board):
            maxv = min(maxv, maximise(result(board, i)))
        return maxv

def maximise(board):
    if terminal(board):
        return utility(board)
    else:
        minv = - math.inf
        for i in actions(board):
            minv = max(minv, minimise(result(board, i)))
        return minv


def minimax(board):
    if terminal(board):
        return None
    if player(board) == O:
        s = math.inf
        best = ()
        for i in actions(board):
            maxv = maximise(result(board, i))
            if maxv < s:
                s = maxv
                best = i
        return best
    else:
        s = - math.inf
        best = ()
        for i in actions(board):
            minv = minimise(result(board, i))
            if minv > s:
                s = minv
                best = i
        return best
