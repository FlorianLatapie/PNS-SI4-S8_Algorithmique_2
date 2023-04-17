SKILL_LEVEL = 5

ROW_COUNT = 6
COLUMN_COUNT = 7
BOARD_SIZE = ROW_COUNT * COLUMN_COUNT

PLAYER_HUMAN = 1
PLAYER_AI = 2

EMPTY = 0
HUMAN_TOKEN = PLAYER_HUMAN
AI_TOKEN = PLAYER_AI

S_EMPTY = str(EMPTY)
S_HUMAN_TOKEN = str(HUMAN_TOKEN)
S_AI_TOKEN = str(AI_TOKEN)

S_HUMAN_TOKEN_4 = S_HUMAN_TOKEN * 4
S_AI_TOKEN_4 = S_AI_TOKEN * 4

STRIDE_LENGTH = 4


class Board:
    def __init__(self, s: str = None):
        """ Is s is not empty, it must be a string enumerating the cells content, column by column
        and starting from the bottom-left corner.

        Each cell is represented by a single character:
        - '0' : empty
        - '1', 'p' or 'h' : player (aka "human")
        - '2', 'a' or 'm' : AI (aka "machine")
        """
        if s:
            s = s.lower().replace('h', '1').replace('m', '2')
            cols = [
                s[start:start + ROW_COUNT]
                for start in range(0, BOARD_SIZE, ROW_COUNT)
            ]

            self._cells = [[int(t) for t in row] for row in zip(*cols)]
            self._column_heights = [len(col.replace('0', '')) for col in cols]
            self._update_columns()

        else:
            self._cells = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
            self._column_heights = [0] * COLUMN_COUNT
            self._columns = [[0] * ROW_COUNT for _ in range(COLUMN_COUNT)]

    @classmethod
    def from_string(cls, s: str) -> 'Board':
        """ Convenience factory method, in case of...
        """
        return Board(s)

    @property
    def rows(self) -> list[list[int]]:
        return self._cells

    def _update_columns(self):
        self._columns = [list(_) for _ in zip(*self._cells)]

    @property
    def columns(self) -> list[list[int]]:
        return self._columns

    def drop_token(self, column_index: int, token: int):
        top = self._column_heights[column_index]
        self._columns[column_index][top] = self._cells[top][column_index] = token
        self._column_heights[column_index] += 1

    def can_play_in_column(self, column_index: int) -> bool:
        return self._column_heights[column_index] < ROW_COUNT

    def get_playable_columns(self) -> list[int]:
        return [c for c in range(COLUMN_COUNT) if self.can_play_in_column(c)]

    def show(self, label: str = None, player_repr='p', ai_repr='a', empty_repr='.'):
        if label:
            print(label)
        reprs = {
            0: empty_repr,
            1: player_repr,
            2: ai_repr
        }
        for row in self._cells[::-1]:
            print(' '.join(reprs[cell] for cell in row))

    def is_winning_move(self, token: int) -> bool:
        board = self._cells

        s_rows = [''.join(str(token) for token in row) for row in self.rows]
        s_columns = [''.join(str(token) for token in column) for column in self.columns]
        wining_stride = str(token) * 4

        # Check horizontal locations for win
        if any(wining_stride in row for row in s_rows):
            return True

        # Check vertical locations for win
        if any(wining_stride in column for column in s_columns):
            return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if all(board[r + i][c + i] == token for i in range(4)):
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if all(board[r - i][c + i] == token for i in range(4)):
                    return True

        return False

    def get_score(self, token: int) -> int:
        board = self._cells
        score = 0

        # Score center column_index
        center_column = COLUMN_COUNT // 2
        center_array = self._columns[center_column]
        center_count = center_array.count(token)
        score += center_count * 3

        # Score Horizontal
        for row_array in self.rows:
            for c in range(COLUMN_COUNT - 3):
                stride = row_array[c:c + STRIDE_LENGTH]
                score += self.get_sequence_value(stride, token)

        # Score Vertical
        for col_array in self.columns:
            for r in range(ROW_COUNT - 3):
                stride = col_array[r:r + STRIDE_LENGTH]
                score += self.get_sequence_value(stride, token)

        # Score positive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                stride = [board[r + i][c + i] for i in range(STRIDE_LENGTH)]
                score += self.get_sequence_value(stride, token)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                stride = [board[r + 3 - i][c + i] for i in range(STRIDE_LENGTH)]
                score += self.get_sequence_value(stride, token)

        return score

    @staticmethod
    def get_sequence_value(sequence: list[int], player: int) -> int:
        s_seq = ''.join(str(_) for _ in sequence)
        if player == HUMAN_TOKEN:
            player_token_4, opp_token_4 = S_HUMAN_TOKEN_4, S_AI_TOKEN_4
        else:
            player_token_4, opp_token_4 = S_AI_TOKEN_4, S_HUMAN_TOKEN_4

        # sequence is all our tokens
        if s_seq == player_token_4:
            return 100

        # 3 of ours contiguous and an empty slot
        if player_token_4[:4] in s_seq and '0' in s_seq:
            return 5

        # 2 of ours contiguous and the rest empty
        if player_token_4[:3] in s_seq and sequence.count(EMPTY) == 2:
            return 2

        # opponent is about to win with 3 contiguous and an empty slot
        if player_token_4[:4] in s_seq and '0' in s_seq:
            return -4

        return 0

    def is_terminal_state(self) -> bool:
        return self.is_winning_move(HUMAN_TOKEN) or self.is_winning_move(AI_TOKEN) or not self.get_playable_columns()
