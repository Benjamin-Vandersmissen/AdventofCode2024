from functools import lru_cache
import copy
data = open('day19').read().splitlines()

towels = [t.strip() for t in data[0].split(',')]
combos = data[2:]

@lru_cache(maxsize=None)
def can_match(combo):
    if combo == '':
        return True

    possible_match = False
    for i in range(1, len(combo)+1):
        if combo[:i] in towels:
            possible_match |= can_match(combo[i:])
    return possible_match

@lru_cache(maxsize=None)
def all_matches(combo):
    if combo == '':
        return 1

    possible_matches = 0
    for i in range(1, len(combo)+1):
        if combo[:i] in towels:
            possible_matches += all_matches(combo[i:])
    return possible_matches


possible = 0
for combo in combos:
    possible += can_match(combo)

print(possible)

matches = 0
for combo in combos:
    matches += all_matches(combo)

print(matches)