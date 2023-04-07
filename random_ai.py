import random
import re

__is_game_over_regex = re.compile('0')

def is_column_available(input: str) -> bool:
    if(__is_game_over_regex.match(input)): return True
    return False

def random_ai_play(input_grid_str: str) -> int:
    random_start = random.randrange(0, 6, 1)
    for i in range(0, 6):
        column = ((random_start + i) % 7)
        if(is_column_available(input_grid_str[column])): return column
    return -1

if __name__ == '__main__':
    example1 = "m00000h00000mm0000hmh000h00000h00000000000"
    res = random_ai_play(example1)

