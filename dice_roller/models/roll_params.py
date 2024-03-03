from pydantic import BaseModel, Field, model_validator

from ..enums.reroll_type import ReRollType
from ..errors import ContradictingThresholdsError


class RollParams(BaseModel):
    diff: int = Field(5, ge=0)
    success_threshold: int = Field(1, ge=1)
    crit_on: int = Field(8, ge=1)
    botch_on: int = Field(1, ge=0)
    re_rolls_allowed: ReRollType = ReRollType.NONE
    re_rolls_amount: int = Field(0, ge=0)
    can_fail: bool = True

    @model_validator(mode="after")
    def validate(self):
        if self.crit_on < self.diff or self.diff < self.botch_on:
            raise ContradictingThresholdsError
