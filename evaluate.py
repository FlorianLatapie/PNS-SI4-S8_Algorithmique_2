def evaluate_logic(board: list):
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

    for board_line in board90:
        line = "".join(board_line)
        score += find_winning_moves_on_a_line(line)

    for board in boards:
        board_length = len(board)
        for line_index, line in enumerate(board):
            line = "".join(line)
            score += find_winning_moves_on_a_line(line) * (board_length - line_index)

    return score


def find_winning_moves_on_a_line(line_of_connect4: str):
    known_winning_moves_human1 = [
        ["1000", "0100", "0010", "0001"],
        ["1100", "0110", "0011", "1010", "0101", "1001"],
        ["0111", "1011", "1101", "1110"],
    ]
    known_winning_moves_machine2 = [
        ["2000", "0200", "0020", "0002"],
        ["2200", "0220", "0022", "2020", "0202", "2002"],
        ["0222", "2022", "2202", "2220"],
    ]

    score = 0

    for move_class_index, move_class in enumerate(known_winning_moves_human1):
        for move in move_class:
            if line_of_connect4.find("1111") != -1:
                score -= 100000
            index = line_of_connect4.find(move)
            if index != -1:
                score -= 1 ** (move_class_index + 1)

    for move_class_index, move_class in enumerate(known_winning_moves_machine2):
        for move in move_class:
            if line_of_connect4.find("2222") != -1:
                score += 100
            index = line_of_connect4.find(move)
            if index != -1:
                score += 1 * (move_class_index + 1)

    return score


def rotate_90(board: list):
    return list(zip(*board[::-1]))


def rotate45(board: list):
    out = []
    for board_line in board:
        for index, cell in enumerate(board_line):
            if len(out) <= index:
                out.append([])
            out[index].append(cell)
    return out


def rotate_minus_45(board: list):
    out = []
    offset = 6
    for board_line_index, board_line in enumerate(board):
        for index, cell in enumerate(board_line):
            index = board_line_index - index + offset
            if len(out) <= index:
                for _ in range(len(out), index + 1):
                    out.append([])
            out[index].append(cell)
    return out
