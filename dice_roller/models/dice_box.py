from dice_roller.enums.d_size import DSize
from dice_roller.models.dice import Dice


class DiceBox:
    @staticmethod
    def dice(d: DSize = DSize.D8) -> Dice:
        return eval(f"D{d.value}()")

    @staticmethod
    def dices(n: int = 1, d: DSize = DSize.D8) -> list[Dice]:
        return [DiceBox.dice(d=d) for _ in range(n)]
