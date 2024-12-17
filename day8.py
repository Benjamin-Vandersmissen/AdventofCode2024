from collections import defaultdict
import itertools

with open('day8') as f:
    data = f.read().splitlines()

antenas = defaultdict(list)
for y, row in enumerate(data):
    for x, val in enumerate(data[y]):
        if val != '.':
            antenas[val].append((x, y))

height = len(data)
width = len(data[0])

def in_bounds(antinode, width, height):
    x, y = antinode
    return 0<=x<width and 0<=y<height

def find_all_grid_positions(a1, a2, width, height):
    dx, dy = a1[0] - a2[0], a1[1] - a2[1]
    locs = set()
    for i in range(-width, width+1):  # currently a very wide net
        if in_bounds((a1[0]+i*dx, a1[1]+i*dy), width, height):
            locs.add((a1[0]+i*dx, a1[1]+i*dy))
    return locs

antinodes = set()
for val in antenas:
    if len(antenas[val]) > 1:
        for i, a1 in enumerate(antenas[val]):
            for j, a2 in enumerate(antenas[val][i+1:]):
                dx, dy = a1[0]-a2[0], a1[1]-a2[1]
                if in_bounds((a2[0]-dx, a2[1]-dy), width, height):
                    antinodes.add((a2[0]-dx, a2[1]-dy))
                if in_bounds((a1[0]+dx, a1[1]+dy), width, height):
                    antinodes.add((a1[0]+dx, a1[1]+dy))

print(len(antinodes))

antinodes = set()
for val in antenas:
    if len(antenas[val]) > 1:
        for i, a1 in enumerate(antenas[val]):
            for j, a2 in enumerate(antenas[val][i+1:]):
                antinodes.update(find_all_grid_positions(a1, a2, width, height))

print(len(antinodes))