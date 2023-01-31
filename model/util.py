import re

from model.core import Dice

_roll_parse_regex = re.compile("(\d+)d(\d+)")


def parse_roll(roll_spec: str) -> Dice:
    result = _roll_parse_regex.search(roll_spec)

    if len(result.groups()) < 2:
        raise Exception(f"Dice roll {roll_spec} is malformed.")

    num_dice, sides = result.groups()
    return Dice(sides=int(sides), num_dice=int(num_dice))
