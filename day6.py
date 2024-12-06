import numpy as np
import copy

with open('day6') as f:
    data = f.read().split()

def update_dir(cur_dir):
    if cur_dir == (1,0):
        return (0, 1)
    elif cur_dir == (0,1):
        return (-1, 0)
    elif cur_dir == (-1,0):
        return (0, -1)
    elif cur_dir == (0,-1):
        return (1, 0)


w, h = len(data[0]), len(data)
grid = np.zeros((w, h))  # W x H grid
visited_grid = np.zeros((w, h))

guard_pos = 0, 0
guard_dir = 0, -1
for y, row in enumerate(data):
    for x, val in enumerate(row):
        grid[x, y] = int(val == '#')
        if val == '^':
            guard_pos = x, y

orig_pos, orig_dir = copy.deepcopy(guard_pos), copy.deepcopy(guard_dir)

already_visited = set()
already_visited.add(guard_pos)
while True:
    new_pos = tuple([p+d for p, d in zip(guard_pos, guard_dir)])
    if not(0 <= new_pos[0] < w and 0 <= new_pos[1] < h):
        break

    if grid[new_pos]:
        guard_dir = update_dir(guard_dir)
        continue

    guard_pos = new_pos
    already_visited.add(guard_pos)
    visited_grid[guard_pos] = 1

print(len(already_visited))

# Expensive brute force
all_locations = set()
for xx in range(w):
    for yy in range(h):
        new_grid = copy.deepcopy(grid)
        already_visited = set()
        guard_pos, guard_dir = copy.deepcopy(orig_pos), copy.deepcopy(orig_dir)
        already_visited.add((guard_pos, guard_dir))

        if new_grid[xx,yy] or (xx, yy) == guard_pos:
            continue
        else:
            new_grid[xx][yy] = 1

        while True:
            new_pos = tuple([p+d for p, d in zip(guard_pos, guard_dir)])
            if not(0 <= new_pos[0] < w and 0 <= new_pos[1] < h):
                break

            if new_grid[new_pos]:
                guard_dir = update_dir(guard_dir)
                continue

            guard_pos = new_pos
            if (guard_pos, guard_dir) in already_visited:
                all_locations.add((xx, yy))
                break
            already_visited.add((guard_pos, guard_dir))
            visited_grid[guard_pos] = 1

print(len(all_locations))
    #
# possible_obstructions = 0  # Find positions such that there is a loop. Meaning that 3 of the 4 points are already present
#
# for pos, dir in obstructions:
#     object_loc = tuple([p+d for p, d in zip(pos,dir)])
#     new_dir = update_dir(dir)
#     new_pos = pos
#
#     can_loop = False
#     while 0 <= new_pos[0] < w and 0 <= new_pos[1] < h:  # Find second corner
#         new_pos = tuple([p + d for p, d in zip(new_pos, new_dir)])
#         if (new_pos, new_dir) in obstructions:
#             new_dir = update_dir(new_dir)
#             can_loop = True
#             break
#
#     if not can_loop:
#         continue
#
#     can_loop = False
#
#     while 0 <= new_pos[0] < w and 0 <= new_pos[1] < h:  # Find third corner
#         new_pos = tuple([p + d for p, d in zip(new_pos, new_dir)])
#         if (new_pos, new_dir) in obstructions:
#             new_dir = update_dir(new_dir)
#             can_loop = True
#             break
#
#     if can_loop:
#         if new_dir[1] == 0:
#             obs_pos = (pos[0]+new_dir[0], new_pos[1])
#             not_useful = [(p, new_pos[1]) for p in range(min(pos[0], new_pos[0]), max(pos[0], new_pos[0]) + 1)]
#         elif new_dir[0] == 0:
#             obs_pos = (new_pos[0], pos[1]+new_dir[1])
#             not_useful = [(new_pos[0], p) for p in range(min(pos[1], new_pos[1]), max(pos[1], new_pos[1]) + 1)]
#
#         for nu in not_useful:
#             if (nu, new_dir) in obstructions:
#                 can_loop = False
#                 break
#
#         if can_loop:
#             possible_obstructions += 1
#             print(obs_pos)
#
