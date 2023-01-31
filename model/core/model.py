from enum import Enum
from random import random
from typing import List, TypeVar, Generic

SearchType = TypeVar("SearchType")
ExpressionResolutionType = TypeVar("ExpressionResolutionType")


class RangeUnit(Enum):
    Meters = "meters"


class TargetType(Enum):
    Creature = "creature"
    Object = "object"


class Component(object):
    def __init__(self) -> None:
        pass


class Expression(Component, Generic[ExpressionResolutionType]):
    def __init__(self):
        super().__init__()

    def resolve(self) -> ExpressionResolutionType:
        raise NotImplementedError()

    def explain(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.explain()


class Name(Component):
    def __init__(self, value: str):
        super().__init__()

        self.value = value


class Description(Component):
    def __init__(self, description: str) -> None:
        super().__init__()

        self.description = description


class Tag(Component):
    def __init__(self, value: str) -> None:
        super().__init__()

        self.value = value


class Targets(Component):
    def __init__(self, num_targets: int, types: List[TargetType]) -> None:
        super().__init__()

        self.num_targets = num_targets
        self.types = types


class Duration(Component):
    def __init__(self):
        super().__init__()


class Range(Component):
    def __init__(self, value: int, unit: RangeUnit) -> None:
        super().__init__()

        self.value = value
        self.unit = unit


class Constraint(Component):
    def __init__(self) -> None:
        super().__init__()


class StaticModifier(Expression[int]):
    def __init__(self, value: int) -> None:
        super().__init__()

        self.value = value

    def resolve(self) -> int:
        return self.value

    def explain(self) -> str:
        sign = "+" if self.value >= 0 else "-"
        return f"{sign} {self.value}"


class RollResult(object):
    def __init__(self) -> None:
        self.results: List[int] = list()

    def add(self, result: int) -> None:
        self.results.append(result)

    def sum(self) -> int:
        return sum(self.results)

    def __str__(self) -> str:
        return f"{self.results}"


class Dice(Expression[RollResult]):
    def __init__(self, num_dice: int, sides: int) -> None:
        super().__init__()

        self.sides = sides
        self.num_dice = num_dice

    def resolve(self) -> RollResult:
        result = RollResult()

        for _ in range(self.num_dice):
            result.add(int(random() * self.sides) + 1)

        return result

    def explain(self) -> str:
        return f"{self.num_dice}d{self.sides}"


class DamageType(Component):
    def __init__(self, value: str):
        super().__init__()

        self.value = value


class Damage(Expression[int]):
    def __init__(self, dice: Expression[RollResult], damage_types: List[DamageType],
                 modifiers: List[StaticModifier] = None) -> None:
        super().__init__()

        self.dice = dice
        self.damage_types = damage_types
        self.modifiers = modifiers if modifiers is not None else list()

    def resolve(self) -> int:
        roll_sum = self.dice.resolve().sum()

        for modifier in self.modifiers:
            roll_sum += modifier.value

        return roll_sum

    def _format_modifiers(self):
        output = ""

        for modifier in self.modifiers:
            output += f"{modifier.explain()}"

        return output

    def explain(self) -> str:
        return f"{self.dice.explain()} {self._format_modifiers()} with damage types: {', '.join([dt.value for dt in self.damage_types])}"


class SearchResult(Generic[SearchType]):
    def __init__(self, matched: List[Component]) -> None:
        self.matched = matched

    def expect(self, expected: int) -> "SearchResult":
        if 0 < expected < len(self.matched):
            raise Exception(f"Script contains {len(self.matched)} components but expected {expected}")

        return self

    def first(self) -> SearchType:
        if len(self.matched) > 0:
            return self.matched[0]

        raise Exception("Search result is empty")


class Script(object):
    def __init__(self, components: List[Component]) -> None:
        self.components = components

    def get_by_type(self, search_type: SearchType) -> SearchResult[SearchType]:
        matched: List[Component] = list()

        for component in self.components:
            if type(component) == search_type:
                matched.append(component)

        return SearchResult(matched=matched)
