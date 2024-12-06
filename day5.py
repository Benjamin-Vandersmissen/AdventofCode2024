from collections import defaultdict
import random
with open('day5') as f:
    data = f.read().split()

def is_correct(update):
    global dependency_rules
    correct = True
    for i in range(len(update) - 1, -1, -1):
        after = update[i + 1:]
        required = dependency_rules[update[i]]
        present = [r for r in after if r in required]
        if len(present) != len(after):
            correct = False
            break
    return correct

rules = []
updates = []
for row in data:
    if '|' in row:
        rules.append(list(map(int, row.split('|'))))
    elif ',' in row:
        updates.append(list(map(int, row.split(','))))

dependency_rules = defaultdict(list)
for required, current in rules:
    dependency_rules[required].append(current)

# Part 1 :
sum_of_middles = 0
for update in updates:
    correct = is_correct(update)
    if correct:
        sum_of_middles += update[(len(update)-1)//2]
print(sum_of_middles)

# Part 2:
sum_of_middles = 0
for update in updates:
    correct = is_correct(update)
    if correct:
        continue
    else:
        relevant_rules = [(update[i], [r for r in dependency_rules[update[i]] if r in update]) for i in range(len(update))]  # Only relevant rules
        relevant_rules = sorted(relevant_rules, key=lambda x: -len(x[1]))
        # Each entry will have a unique number of prerequisites from 0..len(update)-1,
        # We sort inversely, and then we can construct the update that satisfies the dependencies
        new_update = [val[0] for val in relevant_rules]
        assert is_correct(new_update)
        sum_of_middles += new_update[(len(new_update)-1)//2]

print(sum_of_middles)

