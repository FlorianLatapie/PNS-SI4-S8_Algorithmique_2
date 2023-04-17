from random import shuffle
from typing import Union

from models import Board, COLUMN_COUNT
from ._base import AbstractStrategy


class DumbStrategy(AbstractStrategy):
    @property
    def description(self) -> str:
        return "randomly pick one of the playable columns"

    def get_move(self, board: Board) -> Union[int, None]:
        columns = list(range(COLUMN_COUNT))
        shuffle(columns)
        for c in columns:
            if board.can_play_in_column(c):
                return c

        return None
