from collections import defaultdict
import copy
from functools import lru_cache

data = open('day23').read().splitlines()
connections = defaultdict(list)
for line in data:
    first, second = line.split('-')
    connections[first].append(second)
    connections[second].append(first)

connections_as_tuples = [line.split('-') for line in data]

def find_in_working_set(cur, working_set, num=3):
    connected_with_size = []
    if len(cur) == num:
        return set([tuple(sorted(cur))])
    for v in working_set:
        all_connected = True
        for computer in cur:
            all_connected &= computer in connections[v]

        if all_connected:
            new_working_set = copy.deepcopy(working_set)
            new_working_set.remove(v)
            connected_with_size += find_in_working_set(cur + [v], new_working_set, num)

    return set(connected_with_size)

def find_all_in_working_set(cur, working_set):
    connected = [tuple(sorted(cur))]
    for v in working_set:
        all_connected = True
        for computer in cur:
            all_connected &= computer in connections[v]

        if all_connected:
            new_working_set = copy.deepcopy(working_set)
            new_working_set.remove(v)
            connected += find_all_in_working_set(cur + [v], new_working_set)

    return set(connected)

def find_connected_component(num=3):
    connected_components = set()
    for key in connections:
        if len(connections[key]) < num:
            continue
        if key[0] != 't':
            continue
        working_set = connections[key]
        connected_components.update(find_in_working_set([key], working_set, num))

    return connected_components

def neighbours(v):
    ret = []
    for conn in connections_as_tuples:
        one, other = conn
        if one == v:
            ret.append(other)
        if other == v:
            ret.append(one)
    return ret


all_cliques = []
def bron_kerboch2(R, P, X):
    global all_cliques
    if len(P) == 0 and len(X) == 0:
        all_cliques.append(R)
        return
    pivot = (P+X)[0]
    for v in [v for v in P if v not in neighbours(pivot)]:
        v_neighbours = neighbours(v)
        bron_kerboch2(sorted(R + [v]), [n for n in v_neighbours if n in P], [n for n in v_neighbours if n in X])
        P.remove(v)
        X.append(v)

print(len(find_connected_component()))

nodes = list(set([conn[0] for conn in connections_as_tuples]))
bron_kerboch2(R=[], P=nodes, X=[])
all_cliques = sorted(all_cliques, key= lambda x: len(x), reverse=True)
print(','.join(sorted(all_cliques[0])))