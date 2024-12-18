import re
import numpy as np
import matplotlib.pyplot as plt
data = open('day14').read().splitlines()

regex = re.compile(r'p=(?P<x>.+),(?P<y>.+) v=(?P<vx>.+),(?P<vy>.+)')

robots = []
for line in data:
    match = re.match(regex, line)
    robots.append(list(map(int, [match.group('x'), match.group('y'), match.group('vx'), match.group('vy')])))

print(robots)
width, height = 101, 103

def simulate(robot, n_steps):
    x, y, vx, vy = robot
    new_x, new_y = x + n_steps*vx, y + n_steps*vy
    return new_x % width, new_y % height, vx, vy

def per_quadrant(robots):
    top_left = len([robot for robot in robots if robot[0] < width//2 and robot[1] < height//2])
    top_right = len([robot for robot in robots if robot[0] > width//2 and robot[1] < height//2])
    bottom_left = len([robot for robot in robots if robot[0] < width//2 and robot[1] > height//2])
    bottom_right = len([robot for robot in robots if robot[0] > width//2 and robot[1] > height//2])
    return top_left*top_right*bottom_left*bottom_right

def draw(robots):
    arr = np.zeros((103, 101))
    for robot in robots:
        x, y, _, _ = robot
        arr[y, x] =1
    return arr

new_robots = [simulate(robot, 100) for robot in robots]
print(per_quadrant(new_robots))

max_x_var = 1e9
best_x = 0
max_y_var = 1e9
best_y = 0
for i in range(103):
    new_robots = [simulate(robot, i) for robot in robots]
    if np.var([r[0] for r in new_robots]) < max_x_var:
        max_x_var = np.var([r[0] for r in new_robots])
        best_x = i
    if np.var([r[1] for r in new_robots]) < max_y_var:
        max_y_var = np.var([r[1] for r in new_robots])
        best_y = i


for i in range(101*103):
    new_robots = [simulate(robot, i) for robot in robots]
    if i % 101 == best_x and i % 103 == best_y:
        print(i)
        arr = draw(new_robots)
        plt.imsave(f'img_{i}.png', arr)