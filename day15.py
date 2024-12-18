import re
import numpy as np

data = open('day15').read()

match = re.match(re.compile('(?P<grid>##[\s\S]*##)\n\n(?P<moves>[<>^v\s]*)'), data[:])
grid_str, moves = match.group('grid'), match.group('moves')

grid_str = grid_str.split('\n')
grid = np.empty((len(grid_str), len(grid_str[0])), dtype=int)
wide_grid = np.empty((len(grid_str), 2*len(grid_str[0])), dtype=int)

for y, row in enumerate(grid_str):
    for x, val in enumerate(row):
        if val == '#':
            grid[y][x] = -1
            wide_grid[y][2*x:2*x+2] = -1
        if val == '.':
            grid[y][x] = 0
            wide_grid[y][2*x:2*x+2] = 0
        if val == 'O':
            grid[y][x] = 1
            wide_grid[y][2*x:2*x+2] = [1,2]
        if val == '@':
            grid[y][x] = 0
            wide_grid[y][2*x:2*x+2] = 0
            robot = y,x
            wide_robot = y, 2*x

moves = [m for m in moves if m != '\n']

def simulate(grid, robot, moves):
    for move in moves:
        y, x = robot
        if move =='v':
            dx, dy = 0, 1
        elif move == '^':
            dx, dy = 0, -1
        elif move == '<':
            dx, dy = -1, 0
        elif move == '>':
            dx, dy = 1, 0

        can_move, movable_part = True, []
        for i in range(1, max(grid.shape)):
            if grid[y+i*dy, x+i*dx] == 0:
                break
            elif grid[y+i*dy, x+i*dx] == 1:
                movable_part.append([y+i*dy, x+i*dx])
            elif grid[y+i*dy, x+i*dx] == -1:
                can_move = False
                break
        if can_move:
            robot = y + dy, x + dx
            if len(movable_part) > 0:
                if dy == 0:
                    min_x, max_x = min(x+2*dx, x+(len(movable_part)+1)*dx), max(x+2*dx, x+(len(movable_part)+1)*dx)
                    grid[y, min_x: max_x+1] = 1
                elif dx == 0:
                    min_y, max_y = min(y+2*dy, y+(len(movable_part)+1)*dy), max(y+2*dy, y+(len(movable_part)+1)*dy)
                    grid[min_y:max_y+1, x] = 1
                grid[y+dy, x+dx] = 0
    return grid, robot

def simulate_wide(grid, robot, moves):
    for n, move in enumerate(moves):
        y, x = robot
        grid[y,x] = 0
        if move =='v':
            dx, dy = 0, 1
        elif move == '^':
            dx, dy = 0, -1
        elif move == '<':
            dx, dy = -1, 0
        elif move == '>':
            dx, dy = 1, 0

        if dy == 0:
            can_move, movable_part = True, []
            for i in range(1, max(grid.shape)):
                if grid[y, x+i*dx] == 0:
                    break
                elif grid[y, x+i*dx] == 1 or grid[y, x+i*dx] == 2:
                    movable_part.append([y, x+i*dx])
                elif grid[y, x+i*dx] == -1:
                    can_move = False
                    break
            if can_move:
                robot = y, x+dx
                if len(movable_part) > 0:
                    min_x, max_x = min(x+2*dx, x+(len(movable_part)+1)*dx), max(x+2*dx, x+(len(movable_part)+1)*dx)
                    grid[y, min_x:max_x+1] = grid[y, min_x-dx:max_x+1-dx]
                    grid[y, x+dx] = 0
        else:
            can_move, to_move, edges = True, [(y,x)], [x]
            for i in range(1, max(grid.shape)):
                # If we move multiple boxes at the same time, we need to check all the edges for the boxes are 0
                if (grid[y+i*dy, edges] == 0).all():
                    break
                elif (grid[y+i*dy, edges] == -1).any():
                    can_move = False
                    break
                else:
                    new_edges = []
                    for req in edges:
                        if grid[y+i*dy, req]:
                            new_edges.append(req)

                        if grid[y+i*dy, req] == 1 and req + 1 not in edges:
                            edges.append(req + 1)

                        if grid[y+i*dy, req] == 2 and req-1 not in edges:
                            edges.append(req-1)
                    edges = new_edges
                to_move += [(y+i*dy, x) for x in edges]

            if can_move:
                temp_grid = np.copy(grid)
                for obj in to_move[::-1]:
                    yy, xx = obj
                    temp_grid[yy,xx] = 0
                    temp_grid[yy+dy, xx] = grid[yy, xx]
                robot = y+dy, x
                grid = temp_grid
        grid[robot[0], robot[1]] = 3
    return grid, robot



grid, robot = simulate(grid, robot, moves)
wide_grid, wide_robot = simulate_wide(wide_grid, wide_robot, moves)

score = 0
boxes = np.where(wide_grid == 1)
for y, x in zip(boxes[0], boxes[1]):
    score += 100*y + x
print(score)