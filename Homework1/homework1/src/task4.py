def calculate_discount(price, discount):
    if discount < 1:
        return price * (1-discount)
    if discount >= 1:
        return price * (1-to_decimal(discount))
    if discount == 0: 
        return price

def to_decimal(x):
    return x/100
