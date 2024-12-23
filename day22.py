from functools import lru_cache
from collections import defaultdict

data = list(map(int, open('day22').read().split('\n')))

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

@lru_cache(maxsize=None)
def next_secret(cur):
    cur = prune(mix(cur, 64*cur))
    cur = prune(mix(cur, cur // 32))
    cur = prune(mix(cur, 2048*cur))
    return cur

sum = 0

sequence_with_prizes = defaultdict(int)

from tqdm import tqdm
for code in tqdm(data):
    cur_sequence = []
    cur_considered = []
    prev_price = code % 10
    for _ in range(2000):
        code = next_secret(code)
        price = code % 10
        cur_sequence.append(price-prev_price)
        prev_price = price
        if len(cur_sequence) >= 4:
            if cur_sequence[-4:] not in cur_considered:
                sequence_with_prizes[tuple(cur_sequence[-4:])] += price
                cur_considered.append(cur_sequence[-4:])

    sum += code

print(sum, max(sequence_with_prizes.values()))