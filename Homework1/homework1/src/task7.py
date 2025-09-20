import pypokedex  # Library to fetch Pokémon data from Pokédex

# List of available Kanto starter Pokémon
STARTERS = ["bulbasaur", "charmander", "squirtle"]

def get_pokemon(name: str):
    """Fetch Pokémon data by name using pypokedex."""
    return pypokedex.get(name=name)

def _humanize(name: str) -> str:
    """Convert hyphenated names to title case with spaces (e.g., 'fire-flying' -> 'Fire Flying')."""
    return name.replace("-", " ").title()

def display_pokemon_info(pokemon) -> None:
    """Display the Pokémon's type(s) in a human-readable format."""
    type_str = ", ".join(_humanize(t) for t in pokemon.types)
    print(f"\nType(s): {type_str}")

def main() -> None:
    """Main function to prompt user to choose a starter and display its info."""
    print("Choose your Kanto starter:")
    for idx, name in enumerate(STARTERS, start=1):
        print(f"  {idx}. {name.title()}")  # Display options with numbering

    selection = None
    while selection not in {"1", "2", "3"}:
        selection = input("Select 1–3: ").strip()  # Validate input

    chosen_name = STARTERS[int(selection) - 1]
    print(f"\nYou chose {chosen_name.title()}!")

    pokemon = get_pokemon(chosen_name)  # Fetch Pokémon data
    display_pokemon_info(pokemon)       # Show type(s)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
