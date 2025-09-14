from homework1.src.task4 import calculate_discount

def test_wholeNumber():
    assert calculate_discount(10, 50) == 5

def test_decimal():
    assert calculate_discount(10, .5) == 5

def test_Zero():
    assert calculate_discount(5.5, 0) == 5.5
