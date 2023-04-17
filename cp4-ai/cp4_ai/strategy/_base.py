import abc
from typing import Union

from models import Board


class AbstractStrategy(abc.ABC):
    @abc.abstractmethod
    def get_move(self, board: Board) -> Union[int, None]:
        """ Given a board configuration, returns the column to play.

        The result is an integer in the [1, 7] range.
        """
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def description(self) -> str:
        return ""
