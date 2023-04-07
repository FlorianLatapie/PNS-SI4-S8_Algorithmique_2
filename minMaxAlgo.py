import math
from utils import *

WIN_GAME_POINTS = math.inf
LOSE_GAME_POINTS = -math.inf

WIDTH = 7
HEIGHT = 6

HUMAN_PLAYER_REPRESENTATION = 1
MACHIN_PLAYER_REPRESENTATION = 2

def play_move(board):
    depth = 3
    position_to_play = min_max_init(board, depth)
    board[position_to_play[1]][position_to_play[0]] = MACHIN_PLAYER_REPRESENTATION
    return board


def min_max_init(board, depth):
    alpha = math.inf
    beta = -math.inf
    best_score = -math.inf
    best_move = None

    for move in possible_moves(board):
        board_copy = array_copy(board)
        board_copy[move[1]][move[0]] = MACHIN_PLAYER_REPRESENTATION
        score = min_max(board_copy, depth - 1, False, alpha, beta)
        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, best_score)
        if beta <= alpha:
            break

    return best_move


def min_max(board, depth, is_maximizing_player, alpha, beta) :
    if is_game_over(board) or depth == 0:
        return evaluate(board)
    else:
        if is_maximizing_player:
            best_score = -math.inf
            for move in possible_moves(board):
                board_copy = array_copy(board)
                board_copy[move[1]][move[0]] = MACHIN_PLAYER_REPRESENTATION
                score = min_max(board_copy, depth - 1, False, alpha, beta)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = math.inf
            for move in possible_moves(board):
                board_copy = array_copy(board)
                board_copy[move[1]][move[0]] = HUMAN_PLAYER_REPRESENTATION
                score = min_max(board_copy, depth - 1, True, alpha, beta)
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

def possible_moves(board):
    # return list of possible moves of the forme (column, row) or (x, y)
    moves = []
    middle = 3

    for row in range(HEIGHT-1, -1, -1):
        if board[row][middle] == 0:
            moves.append((middle, row))
            break

    for i in range(1, WIDTH//2 + 1):
        left = middle - i
        right = middle + i

        for row in range(HEIGHT-1, -1, -1):
            if board[row][left] == 0:
                moves.append((left, row))
                break

        for row in range(HEIGHT-1, -1, -1):
            if board[row][right] == 0:
                moves.append((right, row))
                break

    return moves

def array_copy(array):
    return [row[:] for row in array]


