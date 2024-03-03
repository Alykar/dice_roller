from enum import StrEnum


class ReRollType(StrEnum):
    NONE = "none"
    BOTCHES = "botches"
    FAILS = "fails"
    ANY = "any"
