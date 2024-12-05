import numpy as np

with open("day2") as f:
    data = f.readlines()

data = [np.asarray(list(map(int, row.split()))) for row in data]

safe = 0
for row in data:
    adjacency = row[1:] - row[:-1]
    all_same_sign = (adjacency > 0).all() or (adjacency < 0).all()
    safe += all_same_sign and np.logical_and(np.abs(adjacency) >= 1, np.abs(adjacency) <= 3).all()

print(safe)

safe = 0
definitely_unsafe = 0
for row in data:
    adjacency = row[1:] - row[:-1]
    definitely_unsafe = (adjacency > 0).sum() < len(adjacency) - 1 and (adjacency < 0).sum() < len(adjacency) - 1  # More than one sign error
    if definitely_unsafe:
        continue
    all_same_sign = (adjacency > 0).all() or (adjacency < 0).all()
    currently_safe = all_same_sign and np.logical_and(np.abs(adjacency) >= 1, np.abs(adjacency) <= 3).all()
    if currently_safe:
        safe += 1
        continue
    for i in range(len(row) ):
        new_row = np.concatenate([row[:i], row[i + 1:]])
        adjacency = new_row[1:] - new_row[:-1]
        all_same_sign = (adjacency > 0).all() or (adjacency < 0).all()
        if all_same_sign and np.logical_and(np.abs(adjacency) >= 1, np.abs(adjacency) <= 3).all():
            safe += 1
            break

print(safe)