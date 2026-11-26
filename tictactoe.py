"""
Tic Tac Toe Player
"""

import copy
import math

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
    """
    Returns player who has the next turn on a board.
    """
    # Count how many moves each player has made so far
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # X moves first, so it is X's turn whenever both have made equal moves
    if x_count == o_count:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Every empty cell is a possible move
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible.add((i, j))
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Moves are only valid on empty cells inside the board
    if action not in actions(board):
        raise Exception("Invalid action")

    # Copy the board so the original is never modified
    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Every line of three cells that wins the game: rows, columns, diagonals
    lines = []
    for i in range(3):
        lines.append([board[i][0], board[i][1], board[i][2]])
        lines.append([board[0][i], board[1][i], board[2][i]])
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    # A line filled with the same player's mark means that player won
    for line in lines:
        if line[0] is not EMPTY and line[0] == line[1] == line[2]:
            return line[0]

    # No winner: the game is in progress or tied
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # The game is over if someone won
    if winner(board) is not None:
        return True

    # ...or if the board is full (a tie)
    return len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # 1 if X won, -1 if O won, 0 for a tie
    won_by = winner(board)
    if won_by == X:
        return 1
    if won_by == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Nothing to do once the game is over
    if terminal(board):
        return None

    # X tries to maximize the score, O tries to minimize it
    best_action = None
    if player(board) == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action), best_value, math.inf)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action), -math.inf, best_value)
            if value < best_value:
                best_value = value
                best_action = action

    return best_action


def max_value(board, alpha, beta):
    """
    Returns the best score X can force from this board,
    skipping branches that cannot change the final choice (alpha-beta pruning).
    """
    if terminal(board):
        return utility(board)

    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, value)

        # O would never let the game reach this branch, so stop looking
        if alpha >= beta:
            break
    return value


def min_value(board, alpha, beta):
    """
    Returns the best score O can force from this board,
    skipping branches that cannot change the final choice (alpha-beta pruning).
    """
    if terminal(board):
        return utility(board)

    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action), alpha, beta))
        beta = min(beta, value)

        # X would never let the game reach this branch, so stop looking
        if alpha >= beta:
            break
    return value
