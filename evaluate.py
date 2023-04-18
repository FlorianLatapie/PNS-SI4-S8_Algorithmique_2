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

    for i in range(len(known_winning_moves_human1)):
        for j in range(len(known_winning_moves_human1[i])):
            index = line_of_connect4.find(known_winning_moves_human1[i][j])
            if line_of_connect4.find("1111") != -1:
                score -= 100
            if index != -1:
                score -= 4 * (i + 1)

    for i in range(len(known_winning_moves_machine2)):
        for j in range(len(known_winning_moves_machine2[i])):
            index = line_of_connect4.find(known_winning_moves_machine2[i][j])
            if line_of_connect4.find("2222") != -1:
                score += 100
            if index != -1:
                score += 4 * (i + 1)

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
                for _ in range(len(out), index + 1):
                    out.append([])
            out[index].append(board[i][j])
    return out
