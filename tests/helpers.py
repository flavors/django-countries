import random


def random_code(choices, length):
    return ''.join(random.choice(choices) for i in range(length))
