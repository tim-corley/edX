import math

def is_prime(n):
    """Determines if a non-negative integer is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n))+ 1):
        if n % i == 0:
            return False
    return True


# (at Terminal)
# python3
# >>> from prime import is_prime
# >>> is_prime(23)
# True
# >>> is_prime(24)
# False
