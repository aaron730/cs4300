import pypokedex

STARTERS = ["bulbasaur", "charmander", "squirtle"]

def get_pokemon(name: str):
    return pypokedex.get(name=name)

def _humanize(name: str) -> str:
    return name.replace("-", " ").title()

def display_pokemon_info(pokemon) -> None:
    type_str = ", ".join(_humanize(t) for t in pokemon.types)
    print(f"\nType(s): {type_str}")

def main() -> None:
    print("Choose your Kanto starter:")
    for idx, name in enumerate(STARTERS, start=1):
        print(f"  {idx}. {name.title()}")

    selection = None
    while selection not in {"1", "2", "3"}:
        selection = input("Select 1–3: ").strip()

    chosen_name = STARTERS[int(selection) - 1]
    print(f"\nYou chose {chosen_name.title()}!")

    pokemon = get_pokemon(chosen_name)
    display_pokemon_info(pokemon)

if __name__ == "__main__":
    main()
