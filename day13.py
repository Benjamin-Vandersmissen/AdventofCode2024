import numpy as np
import re
data = open('day13').read().splitlines()

button_regex = re.compile('.*: X\+(?P<x>\d+), Y\+(?P<y>\d+)')
prize_regex = re.compile('.*: X=(?P<x>\d+), Y=(?P<y>\d+)')

equations = [[]]
for line in data:
    if 'Button' in line:
        match = re.match(button_regex, line)
        equations[-1].append([float(match.group('x')), float(match.group('y'))])
    elif 'Prize' in line:
        match = re.match(prize_regex, line)
        equations[-1].append([float(match.group('x')), float(match.group('y'))])
    else:
        equations.append([])
        continue

cost = 0
for eq in equations:
    lh = np.asarray(eq[:2]).T
    rh = np.asarray(eq[2])
    sol = np.linalg.solve(lh,rh)
    if np.isclose(sol, np.round(sol), atol=1e-3, rtol=0).all() and (sol <= 100).all() and (sol > 0).all():
        cost += 3*sol[0] + sol[1]
    else:
        continue
print(cost)

cost = 0
for eq in equations:
    lh = np.asarray(eq[:2], dtype=np.float64).T
    rh = np.asarray(eq[2], dtype=np.float64) + 10000000000000
    sol = np.linalg.solve(lh,rh)
    if np.isclose(sol, np.round(sol), rtol=0, atol=1e-3).all() and (sol > 0).all():
        cost += 3*sol[0] + sol[1]
    else:
        continue
print(cost)