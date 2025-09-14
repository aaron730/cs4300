from homework1.src.task3 import postitiveOrNegative, printPrimes, whileSum

def test_postitiveOrNegative():
    assert postitiveOrNegative(10) == "Postive"
    assert postitiveOrNegative(-5) == "Negative"
    assert postitiveOrNegative(0) == "Zero"

def test_printPrimes():
    primes = printPrimes()
    print(primes)
    assert len(primes) == 10
    for p in primes:
        assert p > 1
        for i in range(2, int(p ** 0.5) + 1):
            assert p % i != 0

def test_whileSum():
    sum = whileSum
    print(sum)
    assert whileSum() == 5050

