from typing import Union
import random
import math
from copy import deepcopy
import time

from models import Board, AI_TOKEN, HUMAN_TOKEN
from log import LogMgr

from ._base import AbstractStrategy


logger = LogMgr.setup()


class MinMaxStrategy(AbstractStrategy):
    SEARCH_DEPTH = None

    calls_count = 0

    def __init__(self, verbose=True):
        if not self.SEARCH_DEPTH:
            raise NotImplementedError("cannot instantiate MinMaxStrategy directly")

        self.verbose = verbose

    @property
    def description(self) -> str:
        return f"use a {self.SEARCH_DEPTH} levels deep MinMax search of best moves"

    def minimax(self, board: Board, depth, alpha, beta, is_maximizing) -> (int, int):
        # print(f"minimax: depth={depth} alpha={alpha} beta={beta} maximizing={is_maximizing}")
        # print_board(board)
        self.calls_count += 1

        valid_locations = board.get_playable_columns()

        if board.is_terminal_state():
            if board.is_winning_move(AI_TOKEN):
                # print('AI winning move')
                return None, math.inf
            elif board.is_winning_move(HUMAN_TOKEN):
                # print('Human winning move')
                return None, -math.inf
            else:  # Game is over, no more valid moves
                # print("null game")
                return None, 0

        elif depth == 0:
            return None, board.get_score(AI_TOKEN)

        if is_maximizing:
            value = -math.inf
            selected_column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = deepcopy(board)
                b_copy.drop_token(col, AI_TOKEN)
                _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)
                # print(f"{new_score=}")
                if new_score > value:
                    value = new_score
                    selected_column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return selected_column, value

        else:  # Minimizing player
            value = math.inf
            selected_column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = deepcopy(board)
                b_copy.drop_token(col, HUMAN_TOKEN)
                _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)
                # print(f"{new_score=}")
                if new_score < value:
                    value = new_score
                    selected_column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return selected_column, value

    def get_move(self, board: Board) -> Union[int, None]:
        self.calls_count = 0
        started_at = time.time()

        column_index, _ = self.minimax(board, self.SEARCH_DEPTH, -math.inf, math.inf, True)
        if column_index is None:
            return None

        # we used 0-based column index in the computation, but the result is expected to use
        # a "natural" 1-based numbering.
        column_number = column_index + 1

        elapsed = time.time() - started_at
        if self.verbose:
            logger.info("column=%d / calls count=%d / search time=%.3fs", column_number, self.calls_count, elapsed)

        return column_number


class MediumStrategy(MinMaxStrategy):
    SEARCH_DEPTH = 2


class AdvancedStrategy(MinMaxStrategy):
    SEARCH_DEPTH = 4


class ExpertStrategy(MinMaxStrategy):
    SEARCH_DEPTH = 6
