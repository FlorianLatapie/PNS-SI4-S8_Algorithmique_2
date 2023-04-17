from typing import Union
import random

from models import Board, COLUMN_COUNT
from log import LogMgr

from ._base import AbstractStrategy


logger = LogMgr.setup()


class BasicStrategy(AbstractStrategy):
    @property
    def description(self) -> str:
        return "try to detect opponent winning positions"

    def _block_vertical_alignment(self, board: Board, choices: list[int]) -> Union[int, None]:
        logger.info("check potential vertical alignment in columns %s", choices)
        columns = board.columns
        for c in choices:
            column = ''.join(str(token) for token in columns[c])
            logger.info(">>> analyzing column %d (%s)", c + 1, column)
            tokens = column.replace('0', '')
            logger.info("... tokens: %s", tokens)
            if tokens and tokens[-1] == 'h':
                logger.info("... human's token on top")
                bottom = tokens.rfind('m') + 1 if 'm' in tokens else 0
                human_count = len(tokens) - bottom
                if human_count == 3:
                    logger.info("... block column")
                    return c + 1

        return None

    def _block_horizontal_alignment(self, board: Board, choices: list[int]) -> Union[int, None]:
        logger.info("check potential horizontal alignment")
        # scan the board row by row
        for ndx, row in board.rows:
            content = ''.join(str(token) for token in row)
            logger.info(">>> analyzing row %d (%s)", ndx + 1, content)
            if (ndx := content.find('0111')) != -1:
                logger.info('... block start of 3 alignment')
                return ndx + 1
            if (ndx := content.find('1110')) != -1:
                logger.info('... block end of 3 alignment')
                return ndx + 4
            if (ndx := content.find('0110')) != -1:
                logger.info('... block start of double-open 2 alignment')
                return ndx + 1
            if (ndx := content.find('1101')) != -1:
                logger.info('... block hollowed 2-1 pattern')
                return ndx + 3
            if (ndx := content.find('1011')) != -1:
                logger.info('... block hollowed 1-2 pattern')
                return ndx + 2

        return None

    def _try_potential_win(self, board: Board, choices: list[int]) -> Union[int, None]:
        logger.info("look for winning vertical alignment in columns %s", choices)
        columns = board.columns
        for c in choices:
            column = ''.join(str(token) for token in columns[c])
            logger.info(">>> analyzing column %d (%s)", c + 1, column)
            tokens = column.replace('0', '')
            logger.info("... tokens: %s", tokens)
            if tokens and tokens[-1] == '2':
                logger.info("... machine's token on top")
                bottom = tokens.rfind('1') + 1 if '1' in tokens else 0
                human_count = len(tokens) - bottom
                if human_count == 3:
                    logger.info("... terminate alignment")
                    return c + 1

        return None

    def get_move(self, board: Board) -> Union[int, None]:
        # build the list of selectable columns, i.e. those with still room for tokens
        for c in range(COLUMN_COUNT):
            logger.info("#%d > %s", c, board.columns[c])

        choices = board.get_playable_columns()
        logger.info("playable columns: %s", ', '.join(str(c + 1) for c in board.get_playable_columns()))

        selected_column = self._block_vertical_alignment(board, choices)

        if selected_column is None:
            selected_column = self._block_horizontal_alignment(board, choices)

        if selected_column is None:
            selected_column = self._try_potential_win(board, choices)

        if selected_column is None:
            logger.info("play a random opened column")
            selected_column = random.choice(choices) + 1 if choices else None

        logger.info("--> play in column %d", selected_column)
        return selected_column
