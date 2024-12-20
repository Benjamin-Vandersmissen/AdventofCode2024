from functools import lru_cache

import numpy as np

data = open('day20').read().splitlines()
grid = np.empty((len(data), len(data[0])))

start, end = None, None
for y, row in enumerate(data):
    for x, char in enumerate(row):
        if char == '#':
            grid[y, x] = 1
        else:
            grid[y, x] = 0
        if char == 'S':
            start = y, x
        if char == 'E':
            end = y, x


# First get from every position in the grid the fastest way to the end (via bfs)

queue = [(end, 0)]
fastest_to_end = {}
while queue:
    pos, timestep = queue.pop(0)
    fastest_to_end[pos] = timestep
    y, x = pos
    if 0 < y and (y-1, x) not in fastest_to_end and grid[y-1 , x] == 0:
        queue.append(((y-1, x), timestep+1))
    if y < grid.shape[0]-1 and (y+1, x) not in fastest_to_end and grid[y+1 , x] == 0:
        queue.append(((y+1, x), timestep+1))
    if 0 < x and (y, x-1) not in fastest_to_end and grid[y, x-1] == 0:
        queue.append(((y, x-1), timestep+1))
    if x < grid.shape[1]-1 and (y, x+1) not in fastest_to_end  and grid[y , x+1] == 0:
        queue.append(((y, x+1), timestep+1))

    queue = sorted(set(queue), key=lambda x: x[1])

# OLD inefficient code, only useful for the case where cheats are small.
def possible_cheat(path, timesteps=2):
    y, x = path[-1]
    new_paths = []
    if timesteps > 0:  # Explore blocked location
        if 0 < y and grid[y-1 , x] == 1:
            new_paths += possible_cheat(path + [(y-1, x)], timesteps-1)
        if y < grid.shape[0]-1 and grid[y+1 , x] == 1:
            new_paths += possible_cheat(path + [(y+1, x)], timesteps-1)
        if 0 < x and grid[y, x-1] == 1:
            new_paths += possible_cheat(path + [(y, x-1)], timesteps-1)
        if x < grid.shape[1]-1 and grid[y, x+1] == 1:
            new_paths += possible_cheat(path + [(y, x+1)], timesteps-1)
    else: # Always go back to an unblocked location.
        if 0 < y and grid[y-1, x] == 0:
            new_paths += [path + [(y-1, x)]]
        if y < grid.shape[0]-1 and grid[y+1, x] == 0:
            new_paths += [path + [(y+1, x)]]
        if 0 < x and grid[y, x-1] == 0:
            new_paths += [path + [(y, x-1)]]
        if x < grid.shape[1]-1 and grid[y, x+1] == 0:
            new_paths += [path + [(y, x+1)]]

    return new_paths


# all_cheats = []
# for y in range(grid.shape[0]):
#     for x in range(grid.shape[1]):
#         if grid[y, x] == 0:
#             all_cheats += [c for duration in range(1, permissable_cheat_duration) for c in possible_cheat([(y, x)], timesteps=duration)]
# print(len(all_cheats))


import tqdm
from collections import Counter

all_time_saves = []
durations = Counter()
max_cheat_duration = 2
min_time_save = 100
for (y,x) in tqdm.tqdm(fastest_to_end):
    for (y2, x2) in fastest_to_end:
        distance = abs(y-y2) + abs(x-x2)
        if distance <= max_cheat_duration and fastest_to_end[y, x] > fastest_to_end[y2, x2] + distance -1 + min_time_save:
            duration = fastest_to_end[y, x] - fastest_to_end[y2, x2] - distance
            all_time_saves.append([(y,x), (y2, x2)])
            durations[duration] += 1
print(len(all_time_saves), durations.most_common(len(durations)))