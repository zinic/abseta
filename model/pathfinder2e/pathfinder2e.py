from model.core import Script, Name, Damage


def cast_spell(script: Script):
    name = script.get_by_type(search_type=Name).expect(expected=1).first()
    damage = script.get_by_type(search_type=Damage).expect(expected=1).first()

    print(f"Casting spell {name.value}. Roll: {damage.explain()} -> {damage.resolve()}")
