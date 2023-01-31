from model import parse_roll
from model.core import *
from model.pathfinder2e import *


def main() -> None:
    acid_damage_type = DamageType(value="Acid")

    cast_spell(Script([
        Name(
            value="Acid Splash",
        ),
        Description(
            description="You splash a glob of acid that splatters creatures and objects alike. Make a spell attack. If you hit, you deal 1d6 acid damage plus 1 splash acid damage. On a critical success, the target also takes 1 persistent acid damage.",
        ),

        Tag("Acid"),
        Tag("Attack"),
        Tag("Cantrip"),
        Tag("Evocation"),

        Range(
            value=10,
            unit=RangeUnit.Meters,
        ),
        Targets(
            num_targets=1,
            types=[
                TargetType.Creature,
                TargetType.Object,
            ],
        ),

        Damage(
            dice=parse_roll("1d6"),
            damage_types=[
                acid_damage_type,
            ],
            modifiers=[
                StaticModifier(value=1),
            ],
        ),
    ]))


if __name__ == "__main__":
    main()
