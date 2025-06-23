import random

def simulate_random_sets(trials=1000):
    sets = []
    for _ in range(trials):
        s = random.sample(range(1, 46), 6)
        sets.append(sorted(s))
    return sets
