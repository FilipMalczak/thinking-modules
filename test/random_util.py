import random


def random_other_than(*x, min_=0, max_=0xDEADBEEF):
    out = None
    while out is None or out in x:
        out = random.randint(min_, max_)
    return out