filemap = open('day9').read()

filesystem = []
for i, c in enumerate(filemap):
    if c == '0':  # skip empties
        continue
    if i % 2:  # Empty
        filesystem.append((-1, int(c)))
    else:
        filesystem.append((i//2, int(c)))

def reorder(filesystem):
    i = 0
    while i < len(filesystem):
        if filesystem[-1][0] == -1:
            filesystem = filesystem[:-1]  # Remove empty block at the end
            continue
        if filesystem[i][0] == -1:  # Only consider empty spaces
            file = filesystem[-1]
            if file[1] > filesystem[i][1]:  # Too large file, move only the blocks that fit in the empty space
                filesystem[i] = (file[0], filesystem[i][1])
                filesystem[-1] = (file[0], file[1]-filesystem[i][1])
            elif file[1] == filesystem[i][1]:  # Large enough file, move into free space and remove from end
                filesystem[i] = file
                filesystem = filesystem[:-1]
            elif file[1] < filesystem[i][1]: # Too small file, move in free space, keep remaining free space, remove from end
                filesystem = filesystem[:i+1] + [(-1, filesystem[i][1]-file[1])] + filesystem[i+1:-1]
                filesystem[i] = file
        i += 1
    return filesystem

def reorder_no_fragmentation(filesystem):
    files = {}
    free_spaces = []
    idx = 0
    for block in filesystem:
        if block[0] == -1:
            free_spaces.append((idx, block[1]))
        else:
            files[block[0]] = (idx, block[1])
        idx += block[1]

    updated_files = {}
    for k in reversed(files):
        moved = False
        for i in range(len(free_spaces)):
            if free_spaces[i][0] >= files[k][0]:  # Do not move to the right
                break
            if free_spaces[i][1] > files[k][1]:
                updated_files[k] = (free_spaces[i][0], files[k][1])
                free_spaces[i] = (free_spaces[i][0] + files[k][1], free_spaces[i][1]-files[k][1])
                moved = True
                break
            elif free_spaces[i][1] == files[k][1]:
                updated_files[k] = (free_spaces[i][0], files[k][1])
                free_spaces.pop(i)
                moved = True
                break

        if not moved:
            updated_files[k] = files[k]
    return updated_files


def checksum(filesystem):
    idx = 0
    chk = 0
    for block in filesystem:
        id, length = block
        chk += id * sum(range(idx, idx+length))
        idx += length
    return chk

def checksum_no_fragment(filesystem):
    chk = 0
    for k, (idx, length) in filesystem.items():
        chk += k*sum(range(idx, idx+length))
    return chk

# print(checksum(reorder(filesystem)))
print(checksum_no_fragment(reorder_no_fragmentation(filesystem)))
