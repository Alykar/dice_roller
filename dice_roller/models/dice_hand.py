import asyncio
from operator import attrgetter

from dice_roller.enums.reroll_type import ReRollType
from dice_roller.enums.roll_result import RollResult
from dice_roller.errors import EmptyHandError, ImpossibleRollError
from dice_roller.models.dice import Dice
from dice_roller.models.roll_params import RollParams


class DiceHand:
    result: int

    def __init__(self, dices: list[Dice], params: RollParams) -> None:
        self.validate_input(dices, params)

        self.dices = dices
        self.diff = params.diff
        self.crit_on = params.crit_on
        self.success_threshold = params.success_threshold
        self.botch_on = params.botch_on
        self.re_rolls_allowed = params.re_rolls_allowed
        self.re_rolls_amount = params.re_rolls_amount
        self.can_fail = params.can_fail

    @staticmethod
    def validate_input(dices: list[Dice], params: RollParams):
        if len(dices) == 0:
            raise EmptyHandError

        if (
            not params.can_fail
            and params.diff > max(dices, key=attrgetter("size")).size
        ):
            raise ImpossibleRollError

    async def roll_dice(self, dice: Dice, re_roll: bool = False) -> RollResult:
        await dice.roll()
        if dice.result is None:
            raise

        if dice.result <= self.botch_on:
            if (
                self.re_rolls_allowed != ReRollType.NONE
                and self.re_rolls_amount > 0
                and not re_roll
            ):
                self.re_rolls_amount -= 1
                return await self.roll_dice(dice, re_roll=True)

            return RollResult.BOTCH

        elif dice.result < self.diff:
            if not self.can_fail and dice.size >= self.diff:
                return await self.roll_dice(dice)

            if (
                self.re_rolls_allowed in (ReRollType.FAILS, ReRollType.ANY)
                and self.re_rolls_amount > 0
                and not re_roll
            ):
                return await self.roll_dice(dice, re_roll=True)

            return RollResult.FAIL

        if dice.result >= self.diff:
            if self.crit_on <= dice.result != self.diff:
                return RollResult.CRIT

            return RollResult.SUCCESS

        return await self.roll_dice(dice)

    async def roll(self) -> int:
        results = await asyncio.gather(*[self.roll_dice(dice) for dice in self.dices])

        self.result = (
            results.count(RollResult.CRIT) * 2
            + results.count(RollResult.SUCCESS)
            - results.count(RollResult.BOTCH)
        )

        return self.result
