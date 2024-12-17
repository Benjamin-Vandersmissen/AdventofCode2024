import numpy as np
from functools import lru_cache

data = open('day10').read().splitlines()

topo_map = np.empty((len(data), len(data[0])))
for y, row in enumerate(data):
    for x, val in enumerate(data[y]):
        topo_map[y, x] = val


@lru_cache(maxsize=None)
def trail_heads(y, x):
    my_reachable = set()
    if topo_map[y, x] == 9:
        return {(y, x)}
    else:
        if y + 1 < topo_map.shape[0] and topo_map[y+1, x] == topo_map[y, x] + 1:
            my_reachable.update(trail_heads(y + 1, x))
        if y - 1 >= 0 and topo_map[y-1, x] == topo_map[y, x] + 1:
            my_reachable.update(trail_heads(y - 1, x))
        if x + 1 < topo_map.shape[1] and topo_map[y, x+1] == topo_map[y, x] + 1:
            my_reachable.update(trail_heads(y, x + 1))
        if x - 1 >= 0 and topo_map[y, x-1] == topo_map[y, x] + 1:
            my_reachable.update(trail_heads(y, x - 1))
    return my_reachable

@lru_cache(maxsize=None)
def routes(y, x):
    my_routes = set()
    if topo_map[y, x] == 9:
        return {((y, x),)}
    else:
        if y + 1 < topo_map.shape[0] and topo_map[y+1, x] == topo_map[y, x] + 1:
            my_routes.update(routes(y + 1, x))
        if y - 1 >= 0 and topo_map[y-1, x] == topo_map[y, x] + 1:
            my_routes.update(routes(y - 1, x))
        if x + 1 < topo_map.shape[1] and topo_map[y, x+1] == topo_map[y, x] + 1:
            my_routes.update(routes(y, x + 1))
        if x - 1 >= 0 and topo_map[y, x-1] == topo_map[y, x] + 1:
            my_routes.update(routes(y, x - 1))

    my_routes = set([tuple([(y,x)] + list(route)) for route in my_routes])
    return my_routes

all_reachable = 0
for y in range(topo_map.shape[0]):
    for x in range(topo_map.shape[1]):
        if topo_map[y, x] == 0:
            all_reachable += len(trail_heads(y, x))
print(all_reachable)

all_routes = 0
for y in range(topo_map.shape[0]):
    for x in range(topo_map.shape[1]):
        if topo_map[y, x] == 0:
            all_routes += len(routes(y, x))

print(all_routes)