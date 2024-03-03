from abc import ABC
from random import randint

from pydantic import BaseModel

from dice_roller.enums.d_size import DSize


class Dice(BaseModel, ABC):
    _result: int | None = None
    _size: DSize

    @property
    def result(self) -> int | None:
        return self._result

    @property
    def size(self) -> int:
        return self._size.value

    async def roll(self) -> int:
        self._result = randint(1, self.size)
        return self._result
