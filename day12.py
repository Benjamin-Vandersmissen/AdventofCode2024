import numpy as np
from scipy.ndimage import label
data = open('day12').read().split('\n')

def perimeter(indices):
    xs, ys = indices
    temp = []
    ret = 0
    for x, y in zip(xs, ys):
        ret += 4
        temp.append((x,y))
        if (x-1, y) in temp:
            ret -= 2  # Remove the shared wall
        if (x+1, y) in temp:
            ret -= 2
        if (x, y-1) in temp:
            ret -= 2
        if (x, y+1) in temp:
            ret -= 2
    return ret

def sides(indices):
    xs, ys = indices
    all_walls = set()
    internal_walls = set()
    for x, y in zip(xs, ys):
        my_walls = {(x-0.5, y), (x+0.5, y), (x, y-0.5), (x, y+0.5)}
        internal_walls.update(my_walls.intersection(all_walls))  # Add to internal_walls if multiple occupy the same wall
        all_walls.update(my_walls)

    external_walls = all_walls - internal_walls
    num_sides = 0
    for (x, y) in zip(xs, ys):
        my_walls = {(x-0.5, y), (x+0.5, y), (x, y-0.5), (x, y+0.5)}
        my_external_walls = my_walls.intersection(external_walls)
        for ext_wall in my_external_walls:
            num_sides += 1
            d_wall = (ext_wall[0] == int(ext_wall[0]), ext_wall[1] == int(ext_wall[1]))
            for i in range(1, max(grid.shape)):
                possible_side = (ext_wall[0] - i*d_wall[0], ext_wall[1] - i*d_wall[1])
                block = (x - i* d_wall[0], y - i* d_wall[1])
                if possible_side in external_walls:
                    if block in list(zip(xs, ys)): # Only connect individual walls in a side if the adjacent walls are of the same block (no Moebius)
                        external_walls.remove(possible_side)
                    else:
                        break
                else:
                    break

            for i in range(1, max(grid.shape)):
                possible_side = (ext_wall[0] + i * d_wall[0], ext_wall[1] + i * d_wall[1])
                block = (x + i * d_wall[0], y + i * d_wall[1])
                if possible_side in external_walls:
                    if block in list(zip(xs, ys)): # Only connect individual walls in a side if the adjacent walls are of the same block (no Moebius)
                        external_walls.remove(possible_side)
                    else:
                        break
                else:
                    break

    return num_sides

grid = np.empty((len(data), len(data[0])), int)
for y, row in enumerate(data):
    for x, c in enumerate(row):
        grid[y, x] = ord(c) - ord('A') + 1

structure = np.asarray([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

cost = 0
for val in np.unique(grid):
    labeled, ncomponents = label(grid == val, structure)
    for i in range(1, ncomponents+1):
        indices = np.where(labeled == i)
        cost += perimeter(indices) * len(indices[0])

print(cost)

cost = 0
for val in np.unique(grid):
    labeled, ncomponents = label(grid == val, structure)
    for i in range(1, ncomponents+1):
        indices = np.where(labeled == i)
        cost += sides(indices) * len(indices[0])

print(cost)