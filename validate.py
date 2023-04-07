def validate_grid(user_input: str):
    if len(user_input) != 42:
        return False

    if (user_input.count('h') - user_input.count('m')) != 1:
        return False

    return True

def conversion_grid(user_input: str):
    grid = []
    for i in range(0, 42, 7):
        grid.append(user_input[i:i+7])
    return grid
