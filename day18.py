from functools import lru_cache

import numpy as np
data = open('day18').read().splitlines()
bytes = [list(map(int, row.split(','))) for row in data]

grid = np.zeros((71, 71), dtype=int)

@lru_cache(maxsize=None)
def grid_at_time(timestep):
    temp_grid = np.copy(grid)
    for i, coor in enumerate(bytes):
        if i >= timestep:
            break
        temp_grid[coor[1], coor[0]] = -1
    return temp_grid


step = len(bytes) / 4
cur = len(bytes) // 2

# Quick binary search
while step > 0.5:
    queue = [((0,0), 0)]
    next_grid = grid_at_time(cur)
    visited = set()
    reached_end = False
    while len(queue) > 0:
        coor, timestep = queue.pop(0)
        visited.add(coor)
        (y, x) = coor

        if x == grid.shape[1] - 1 and y == grid.shape[0] - 1:
            reached_end = True
            break

        # next_grid = grid_at_time(timestep+1)
        if y > 0 and next_grid[y - 1, x] != -1 and (y-1, x) not in visited:
            queue.append(((y-1, x), timestep + 1))
        if y < next_grid.shape[0] -1 and next_grid[y + 1, x] != -1 and (y+1, x) not in visited:
            queue.append(((y+1, x), timestep + 1))
        if x > 0 and next_grid[y, x - 1] != -1  and (y, x-1) not in visited:
            queue.append(((y, x-1), timestep + 1))
        if x < next_grid.shape[0] - 1 and next_grid[y, x + 1] != -1  and (y, x+1) not in visited:
            queue.append(((y, x + 1), timestep + 1))

        queue = sorted(set(queue), key=lambda x: x[1]-(x[0][0] + x[0][1]))
    if reached_end:
        print(f"Reached end after {cur} bytes fell down in {timestep} steps")
        cur += step
        cur = round(cur)
        step /=2
    else:
        print(f"Did not reach end after {cur}")
        cur -= step
        cur = round(cur)
        step /= 2

