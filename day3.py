import re

with open('day3') as f:
    data = f.readlines()

result = 0
for row in data:
    regex = re.compile('mul\((?P<left>\d+),(?P<right>\d+)\)')
    matches = regex.findall(row)
    if matches:
        for l, r in matches:
            result += int(l)*int(r)

print(result)

result = 0
doing = True
for row in data:
    regex = re.compile('mul\((?P<left>\d+),(?P<right>\d+)\)|(?P<do>do\(\))|(?P<dont>don\'t\(\))')
    matches = regex.findall(row)
    if matches:
        for l, r, do, dont in matches:
            if do != '':
                doing = True
            elif dont != '':
                doing = False
            if l != '' and r != '' and doing:
                result += int(l)*int(r)
print(result)
