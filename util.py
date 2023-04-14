def board_pretty_print(board: list, message: str = ''):
    print(message)
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end='')
        print()
    print()