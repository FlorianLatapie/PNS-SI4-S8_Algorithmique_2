import utils

def main(input: str) -> int:
    is_valid = utils.validate_grid(input)
    is_over = utils.is_game_over(input)
    if(not is_valid): print("grid_not_valid")
    if(is_over): print("game_is_over")
    return 0

if __name__ == '__main__':
    example1 = "m00000h00000mm0000hmh000h00000h00000000000"
    example2 = "m00000h00000mm0000hmh000h00000h00000000000"
    main(example1)
