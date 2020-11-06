# Your code here
import random
import math
cache = {}
def djb2(key):
    """
    DJB2 hash, 32-bit
    """
    hash_index = 5381
    hash_bytes = key.encode()

    for byte in hash_bytes:
        hash_index = ((hash_index << 5) + hash_index) + byte

    return hash_index

def slowfun_too_slow(x, y):
    v = math.pow(x, y)
    v = math.factorial(v)
    v //= (x + y)
    v %= 982451653

    return v

def slowfun(x, y):
    """
    Rewrite slowfun_too_slow() in here so that the program produces the same
    output, but completes quickly instead of taking ages to run.
    """
    # Your code here

    key = djb2(f"{x}{y}")

    if key not in cache:
        cache[key] = slowfun_too_slow(x, y)

    return cache[key]

# Do not modify below this line!

for i in range(50000):
    x = random.randrange(2, 14)
    y = random.randrange(3, 6)
    print(f'{i}: {x},{y}: {slowfun(x, y)}')
