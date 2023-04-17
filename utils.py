import re
import evaluate
import logging

NUM_ROWS = 6
NUM_COLUMNS = 7


def board_pretty_print(board: list, message: str = ''):
    print(message)
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end='')
        print()
    print()


__is_game_over_regex = re.compile('0')


def validate_grid(user_input: str) -> bool:
    if len(user_input) != 42:
        return False
    if (user_input.count('h') - user_input.count('m')) != 1:
        return False
    return True


def convert_string_to_grid(user_input: str) -> list[str]:
    parsed_input = user_input.replace("m", "2").replace("h", "1")
    grid = ["", "", "", "", "", ""]
    for x in range(0, 6, 1):
        for y in range(0, 7, 1):
            base = x + 6 * y
            curr = parsed_input[base]
            grid[x] = grid[x] + curr
    return grid


def convert_grid_to_string(grid: list[str]) -> str:
    grid_string = ""
    for y in range(0, NUM_COLUMNS, 1):
        for x in range(0, NUM_ROWS, 1):
            grid_string = grid_string + grid[x][y]
    return grid_string


def is_game_over(arr: str) -> bool:
    for i in range(len(arr)):
        if __is_game_over_regex.match(arr[i]):
            return False
    return True


def replace_str_index(text, index=0, replacement=''):
    return text[:index] + replacement + text[index + 1:]


def add_move_to_grid(grid: str, move: int, player_symbol: str) -> str:
    grid_array = convert_string_to_grid(grid)
    for i in range(NUM_ROWS):
        if grid_array[i][move] == "0":
            grid_array[i] = replace_str_index(grid_array[i], move, player_symbol)
            return convert_grid_to_string(grid_array)
    raise Exception("Move not valid")

def print_grid(grid_str: str):
    grid = convert_string_to_grid(grid_str)
    length = len(grid)
    for i in range(length-1, -1, -1):
        logging.debug(grid[i])

def has_player_won(grid_str: str, player_symbol: str):
    grid = convert_string_to_grid(grid_str)
    board45 = evaluate.rotate45(grid)
    board90 = evaluate.rotate_90(grid)
    board_minus_45 = evaluate.rotate_minus_45(grid)
    boards = [
        grid,
        board45,
        board90,
        board_minus_45
    ]
    for board in boards:
        for j in range(len(board)):
            board_line = "".join(board[j])
            if board_line.find(player_symbol*4) != -1: return True
    return False



# def has_won(line_of_connect4: str):
#     known_winning_moves_human1 = [
#         ["1000", "0100", "0010", "0001"],
#         ["1100", "0110", "0011", "1010", "0101", "1001"],
#         ["0111", "1011", "1101", "1110"],
#     ]
#     known_winning_moves_machine2 = [
#         ["2000", "0200", "0020", "0002"],
#         ["2200", "0220", "0022", "2020", "0202", "2002"],
#         ["0222", "2022", "2202", "2220"],
#     ]
#     score = 0
#     for i in range(len(known_winning_moves_human1)):
#         for j in range(len(known_winning_moves_human1[i])):
#             index = line_of_connect4.find(known_winning_moves_human1[i][j])
#             if line_of_connect4.find("1111") != -1:
#                 score -= 100000
#             if index != -1:
#                 score -= 1 ** (i + 1)
#     for i in range(len(known_winning_moves_machine2)):
#         for j in range(len(known_winning_moves_machine2[i])):
#             index = line_of_connect4.find(known_winning_moves_machine2[i][j])
#             if line_of_connect4.find("2222") != -1:
#                 score += 100
#             if index != -1:
#                 score += 1 * (i + 1)
#     return score
#
#
#
if __name__ == '__main__':
    example1 = "m00000h00000mm0000hmh000h00000h00000000000"
    example2 = "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
    # res = convert_string_to_grid(example1)
    # print(res)
    # print(res)
    # res = add_move_to_grid(example1, 6, "2")
    # res = convert_string_to_grid(res)
    # print(res)
    is_over = is_game_over(example1)
