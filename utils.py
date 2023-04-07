import re

is_over_regex = re.compile('0')
def validate_grid(user_input: str) -> bool:
    if len(user_input) != 42:
        return False
    if (user_input.count('h') - user_input.count('m')) != 1:
        return False
    return True

def conversion_grid(user_input: str) -> list[str]:
    parsed_input = user_input.replace("m", "2").replace("h", "1")
    grid = ["", "", "", "", "", ""]
    for x in range(0, 6, 1):
        for y in range(0, 7, 1):
            base = x + 6 * y
            curr = parsed_input[base]
            grid[x] = grid[x] + curr
    return grid

def is_game_over(arr) -> bool:
    for i in range(len(arr)):
        if(is_over_regex.match(arr[i])): return False
    return True

if __name__ == '__main__':
    example1 = "m00000h00000mm0000hmh000h00000h00000000000"
    example2 = "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
    res = conversion_grid(example1)
    is_over = is_game_over(res)
