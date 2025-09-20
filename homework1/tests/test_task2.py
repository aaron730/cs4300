from src.task2 import get_integer, get_floating, get_string, get_boolean

def test_task2_integer():
    assert isinstance(get_integer(), int)
    assert get_integer() == 2

def test_task2_floating():
    assert isinstance(get_floating(), float)
    assert get_floating() == 2.2

def test_task2_int():
    assert isinstance(get_string(), str)
    assert get_string() == "Two"

def test_task2_boolean():
    assert isinstance(get_boolean(), bool)
    assert get_boolean() is True

