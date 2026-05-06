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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # O X sempre começa. Se as contagens forem iguais, é a vez do X.
    if x_count > o_count:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Ação inválida: esta célula já está ocupada.")

    # Cria uma cópia profunda para não alterar o estado da matriz original
    new_board = copy.deepcopy(board)
    current_player = player(board)

    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checagem de linhas
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O

    # Checagem de colunas
    for j in range(3):
        if (board[0][j] == board[1][j] == board[2][j] and
                board[0][j] is not EMPTY):
            return board[0][j]

    # Checagem das diagonais principais
    if (board[0][0] == board[1][1] == board[2][2] and
            board[0][0] is not EMPTY):
        return board[0][0]

    if (board[0][2] == board[1][1] == board[2][0] and
            board[0][2] is not EMPTY):
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    # Se houver alguma célula vazia, o jogo ainda está em andamento
    for row in board:
        if EMPTY in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    # Jogador X tenta maximizar a pontuação
    if current_player == X:
        best_val = -math.inf
        best_action = None

        for action in actions(board):
            val = min_value(result(board, action))
            if val > best_val:
                best_val = val
                best_action = action

        return best_action

    # Jogador O tenta minimizar a pontuação
    else:
        best_val = math.inf
        best_action = None

        for action in actions(board):
            val = max_value(result(board, action))
            if val < best_val:
                best_val = val
                best_action = action

        return best_action


def max_value(board):
    """
    Função auxiliar que calcula o valor máximo possível na árvore de decisão.
    """
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Função auxiliar que calcula o valor mínimo possível na árvore de decisão.
    """
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v