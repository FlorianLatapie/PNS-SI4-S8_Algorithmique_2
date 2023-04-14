import math
from random import randint

from utils import *

WIN_GAME_POINTS = math.inf
LOSE_GAME_POINTS = -math.inf

WIDTH = 7
HEIGHT = 6

EMPTY_CELL_REPRESENTATION = '0'
HUMAN_PLAYER_REPRESENTATION = '1'
MACHIN_PLAYER_REPRESENTATION = '2'

# Return the column where the player can play beginning at one
def play_move(board):
    depth = 3
    position_to_play = min_max_init(board, depth)
    # Because column start to 1 and not 0 in the API
    return position_to_play[0] + 1


def min_max_init(board, depth):
    alpha = -math.inf
    beta = math.inf
    best_score = -math.inf
    best_move = None

    for move in possible_moves(board):
        board_copy = array_copy(board)
        board_copy[move[1]] = replace_str_index(board_copy[move[1]], move[0], MACHIN_PLAYER_REPRESENTATION)
        score = min_max(board_copy, depth - 1, False, alpha, beta)
        # print("Score: " + str(score) + " Move: " + str(move))
        if score > best_score:
            # print("Better Score: " + str(score) + " Move: " + str(move))
            best_score = score
            best_move = move

        alpha = max(alpha, best_score)
        if beta <= alpha:
            break

    # print("Best score: " + str(best_score) + " Best move: " + str(best_move))
    return best_move


def min_max(board, depth, is_maximizing_player, alpha, beta):
    if is_game_over(board) or depth == 0:
        return evaluate(board)
    else:
        if is_maximizing_player:
            best_score = -math.inf
            print(possible_moves(board))
            for move in possible_moves(board):
                board_copy = array_copy(board)
                board_copy[move[1]] = replace_str_index(board_copy[move[1]], move[0], MACHIN_PLAYER_REPRESENTATION)
                score = min_max(board_copy, depth - 1, False, alpha, beta)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = math.inf
            print(possible_moves(board))
            for move in possible_moves(board):
                board_copy = array_copy(board)
                board_copy[move[1]] = replace_str_index(board_copy[move[1]], move[0], HUMAN_PLAYER_REPRESENTATION)
                score = min_max(board_copy, depth - 1, True, alpha, beta)
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

def possible_moves(board):
    # return list of possible moves of the forme (column, row) or (x, y)
    # print("Board: " + str(board))
    moves = []
    middle = 3

    for row in range(HEIGHT):
        if board[row][middle] == EMPTY_CELL_REPRESENTATION:
            moves.append((middle, row))
            break

    for i in range(1, WIDTH//2 + 1):
        left = middle - i
        right = middle + i

        for row in range(HEIGHT):
            if board[row][left] == EMPTY_CELL_REPRESENTATION:
                moves.append((left, row))
                break

        for row in range(HEIGHT):
            if board[row][right] == EMPTY_CELL_REPRESENTATION:
                moves.append((right, row))
                break
    return moves

def array_copy(array):
    return [row for row in array]

def evaluate(board):
    return randint(-100, 100)


# if __name__=="__main__":
#     a = ["abdgfgz", "ejfzebf"]
#     b = array_copy(a)
#     a[0] = replace_str_index(a[0], 1, "E")
#     print(a)
#     print(b)

