#Return final price after discount; discount < 1 is decimal, >= 1 is percentage
def calculate_discount(price, discount):
    if discount < 1:
        return price * (1-discount)
    if discount >= 1:
        return price * (1-to_decimal(discount))

#Converts number to decimal
def to_decimal(x):
    return x/100
