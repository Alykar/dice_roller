from enum import Enum


class RollResult(Enum):
    CRIT = 2
    SUCCESS = 1
    FAIL = 0
    BOTCH = -1
