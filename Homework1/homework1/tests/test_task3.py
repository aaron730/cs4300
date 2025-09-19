from homework1.src.task3 import postitive_or_negative, print_primes, while_sum

def test_postitive_or_negative():
    assert postitive_or_negative(10) == "Postive"
    assert postitive_or_negative(-5) == "Negative"
    assert postitive_or_negative(0) == "Zero"

def test_print_primes():
    primes = print_primes()
    print(primes)
    assert len(primes) == 10
    for p in primes:
        assert p > 1
        for i in range(2, int(p ** 0.5) + 1):
            assert p % i != 0

def test_while_sum():
    sum = while_sum
    print(sum)
    assert while_sum() == 5050

