from functools import lru_cache
import numpy as np

data = open('day16').read().splitlines()

grid = np.empty((len(data), len(data[0])), int)

start, end = None, None
start_dir = (0, -1)
for y, row in enumerate(data):
    for x, val in enumerate(row):
        if val == '#':
            grid[y, x] = -1
        else:
            grid[y,x] = 0
        if val == 'S':
            start = (y,x)
        if val == 'E':
            end = (y,x)

def rotate(dir, n_rots):
    n_rots = n_rots % 4
    for _ in range(n_rots):
        if dir == (-1, 0):
            dir = (0, -1)
        elif dir == (0, -1):
            dir = (1, 0)
        elif dir == (1, 0):
            dir = (0, 1)
        elif dir == (0, 1):
            dir = (-1, 0)
    return dir


#implement BFS
current_nodes = [(start, start_dir, 0, 0)]
scores = {}

all_best_paths = set()

best_score = -1

last_idx = 1
path_mapping = {0: [start]}

while current_nodes:
    pos, dir, score, cur_idx = current_nodes.pop()
    cur_path = path_mapping.pop(cur_idx)
    scores[pos, dir] = score
    if pos == end:
        if best_score == -1:
            best_score = score
        elif score > best_score:
            print(best_score)
            break
        all_best_paths.update(set(cur_path))
    y, x = pos
    dy, dx = dir
    if grid[y+dy, x+dx] != -1:
        new_node = (y+dy, x+dx)
        current_nodes.append((new_node, dir, score+1, last_idx))
        path_mapping[last_idx] = cur_path + [new_node]
        last_idx += 1
        scores[(new_node, dir)] = score + 1

    rot1 = rotate(dir, 1)
    if (pos, rot1) not in scores or score + 1000 < scores[(pos, rot1)]:
        current_nodes.append((pos, rot1, score+1000, last_idx))
        path_mapping[last_idx] = cur_path
        last_idx += 1
    rot2 = rotate(dir, 2)
    if (pos, rot2) not in scores or score + 2000 < scores[(pos, rot2)]:
        current_nodes.append((pos, rot2, score+2000, last_idx))
        path_mapping[last_idx] = cur_path
        last_idx += 1
    rot3 = rotate(dir, 3)
    if (pos, rot3) not in scores or score + 1000 < scores[(pos, rot3)]:
        current_nodes.append((pos, rot3, score+1000, last_idx))
        path_mapping[last_idx] = cur_path
        last_idx += 1
    current_nodes = sorted(current_nodes, key=lambda v : -v[2])  # -(abs(v[0][0]-end[0]) + abs(v[0][1]-end[1])) heuristic doesn't work

print(len(all_best_paths))
