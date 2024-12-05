from collections import defaultdict
with open('day1') as f:
    data = f.readlines()

left, right = [int(row.split()[0]) for row in data], [int(row.split()[1]) for row in data]
left, right = sorted(left), sorted(right)

distances = [abs(l - r) for l,r in zip(left, right)]
print(sum(distances))

right_counter = defaultdict(int)
for r in right:
    right_counter[r] += 1

sim_score = 0
for num in left:
    sim_score += num * right_counter[num]
print(sim_score)