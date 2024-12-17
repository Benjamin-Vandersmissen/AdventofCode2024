from functools import lru_cache
data = open('day11').read()
stones = data.split(' ')

def easy_implementation(stones):
    new_stones = []
    for stone in stones:
        if stone == '0':
            new_stones.append('1')
        elif len(stone) % 2 == 0:
            new_stones += [stone[:len(stone) // 2], str(int(stone[len(stone) // 2: ]))]  # Convert second part to int to remove leading zeros.
        else:
            new_stones += [str(2024 * int(stone))]

    return new_stones

@lru_cache(maxsize=None)
def cached_implementation(stone, iterations):
    if iterations == 0:
        return 1
    else:
        if stone == '0':
            return cached_implementation('1', iterations - 1)
        elif len(stone) % 2 == 0:
            return (cached_implementation(stone[:len(stone) // 2], iterations - 1) +
                    cached_implementation(str(int(stone[len(stone) // 2: ])), iterations - 1))
        else:
            return cached_implementation(str(2024 * int(stone)), iterations - 1)

# for i in range(25):
#     stones = easy_implementation(stones)
#
# print(len(stones))

n_stones = 0
for stone in stones:
    n_stones += cached_implementation(stone, 75)
print(n_stones)