from util import *

def evaluate(board: list):
    board90 = rotate_90(board)
    board45 = rotate45(board)
    board_minus_45 = rotate_minus_45(board)

    boards = [
        board,  # plus c'est bas plus ca vaut de points [0] difficile, [6] facile
        # board90,
        board45,  # plus c'est bas plus ca vaut de points [0] difficile, [6] facile
        board_minus_45  # plus c'est bas plus ca vaut de points [0] difficile, [6] facile
    ]

    score = 0

    for j in range(len(board90)):
        line = "".join(board90[j])
        score += find_winning_moves_on_a_line(line)

    for i in range(len(boards)):
        board = boards[i]
        for j in range(len(board)):
            line = "".join(board[j])
            score += find_winning_moves_on_a_line(line) * (len(board) - j)

    return score


def find_winning_moves_on_a_line(line_of_connect4: str):
    known_winning_moves_human1 = [
        ["1___", "_1__", "__1_", "___1"],
        ["11__", "_11_", "__11", "1_1_", "_1_1", "1__1"],
        ["_111", "1_11", "11_1", "111_"],
    ]
    known_winning_moves_machine2 = [
        ["2___", "_2__", "__2_", "___2"],
        ["22__", "_22_", "__22", "2_2_", "_2_2", "2__2"],
        ["_222", "2_22", "22_2", "222_"],
    ]

    score = 0

    for i in range(len(known_winning_moves_human1)):
        for j in range(len(known_winning_moves_human1[i])):
            index = line_of_connect4.find(known_winning_moves_human1[i][j])
            if line_of_connect4.find("1111") != -1:
                score -= 100000
            if index != -1:
                score -= 1 ** (i + 1)

    for i in range(len(known_winning_moves_machine2)):
        for j in range(len(known_winning_moves_machine2[i])):
            index = line_of_connect4.find(known_winning_moves_machine2[i][j])
            if line_of_connect4.find("2222") != -1:
                score += 100
            if index != -1:
                score += 1 * (i + 1)

    return score


def rotate_90(board: list):
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            # if out[j] does not exist, create it :
            if len(out) <= j:
                out.append([])

            out[j].append(board[i][j])
    return out


def rotate45(board: list):
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if len(out) <= i + j:
                out.append([])
            out[i + j].append(board[i][j])
    return out


def rotate_minus_45(board: list):
    out = []
    offset = 6
    for i in range(len(board)):
        for j in range(len(board[i])):
            index = i - j + offset
            if len(out) <= index:
                for k in range(len(out), index + 1):
                    out.append([])
            out[index].append(board[i][j])
    return out
