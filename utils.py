import re
NUM_ROWS=6
NUM_COLUMNS=7

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


def is_game_over(arr) -> bool:
    for i in range(len(arr)):
        if(__is_game_over_regex.match(arr[i])): return False
    return True

def replace_str_index(text,index = 0, replacement=''):
    return text[:index] + replacement + text[index + 1:]

def add_move_to_grid(grid: str, move: int, player_symbol: str) -> str:
    grid_array = convert_string_to_grid(grid)
    for i in range(NUM_ROWS):
        if(grid_array[i][move] == "0"): 
            grid_array[i] = replace_str_index(grid_array[i], move, player_symbol)
            return convert_grid_to_string(grid_array)
    raise Exception("Move not valid")


if __name__ == '__main__':
    example1 = "m00000h00000mm0000hmh000h00000h00000000000"
    example2 = "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
    res = convert_string_to_grid(example1)
    print(res)
    print(res)
    res = add_move_to_grid(example1, 6, "2")
    res = convert_string_to_grid(res)
    print(res)
    is_over = is_game_over(res)
