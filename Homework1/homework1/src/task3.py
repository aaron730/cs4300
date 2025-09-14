def postitiveOrNegative(x):
    if x > 0:
        return "Postive"
    elif x < 0:
         return "Negative"
    else:
         return "Zero"


def printPrimes():
    primes = []
    num = 2
    for _ in range(100):
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                break
        else:
            primes.append(num)
            if len(primes) == 10:
                break
        num += 1
    return primes

def whileSum():
    num = 1
    sum = 0
    while(num <= 100):
        sum += num
        num+= 1
    return sum 