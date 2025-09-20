
import homework1.src.task7 as task7

def test_choose_two(monkeypatch, capsys):
    # Mock input to choose "2"
    monkeypatch.setattr("builtins.input", lambda _: "2")

    # Stub get_pokemon to avoid API call
    class FakePokemon:
        types = ["fire"]

    monkeypatch.setattr(task7, "get_pokemon", lambda name: FakePokemon())

    # Run main
    task7.main()

    # Capture output
    out, _ = capsys.readouterr()

    # 
    assert "You chose Charmander" in out
    assert "Type(s): Fire" in out
