from models import Board, HUMAN_TOKEN, AI_TOKEN
from strategy.minmax import AdvancedStrategy, ExpertStrategy


def main():
    board = Board()

    strategy = None
    while not strategy:
        try:
            choice = input("Strategy: A)dvanced or E)xpert ? ")
        except KeyboardInterrupt:
            print('\x08\x08Bye')
            return

        if choice is None:
            print("!! Invalid input. Try again.")

        else:
            choice = choice.upper()
            if choice == 'A':
                strategy = AdvancedStrategy(verbose=False)
            elif choice == 'E':
                strategy = ExpertStrategy(verbose=False)
            else:
                print("!! Invalid input. Try again.")

    board.show("\nOK, let's play together.")

    while not board.is_terminal_state():
        print()
        try:
            resp = input("Your move [1-7] : ")
        except KeyboardInterrupt:
            print('\x08\x08')
            break

        try:
            move = int(resp)
        except ValueError:
            print("!! Invalid input. Try again.")
            continue
        if not 1 <= move <= 7:
            print("!! Invalid column number. Try again.")
            continue

        column_index = move - 1

        if not board.can_play_in_column(column_index):
            print("!! Cannot play in this column. Try again.")
            continue

        board.drop_token(column_index, HUMAN_TOKEN)
        board.show()

        if board.is_winning_move(HUMAN_TOKEN):
            print("\nCongratulation, you won !!")
            break

        ai_move = strategy.get_move(board)

        board.drop_token(ai_move - 1, AI_TOKEN)
        board.show(f"\nI played in column {ai_move} :")

        if board.is_winning_move(AI_TOKEN):
            print("\nSorry, I won !!")
            break

    print("\nBye.")


if __name__ == '__main__':
    main()
