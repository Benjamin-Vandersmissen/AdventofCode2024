import re
with open('day4') as f:
    data = f.read().split()

def regex_match_all(regex, string):
    matches = []
    match = regex.search(string)
    while match:
        matches.append(match)
        match = regex.search(string, match.end())
    matches.append(match)
    return matches

regex = re.compile("XMAS")

n_xmas = sum([len(regex.findall(row)) for row in data])
n_xmas += sum([len(regex.findall(row[::-1])) for row in data])

row_len = len(data[0])
columns = [''.join([row[i] for row in data]) for i in range(row_len)]

modified_grid = [len(row)*'_' + row + len(row)*'-' for row in data] # Pad

rdown_diagonals = [''.join(modified_grid[i][x+i] for i in range(len(data))) for x in range(len(modified_grid[0]) - len(data)+1)]
ldown_diagonals = [''.join(modified_grid[i][x-i] for i in range(len(data))) for x in range(len(data)-1, len(modified_grid[0]))]

n_xmas += sum([len(regex.findall(col)) for col in columns])
n_xmas += sum([len(regex.findall(col[::-1])) for col in columns])

n_xmas += sum([len(regex.findall(diag)) for diag in ldown_diagonals])
n_xmas += sum([len(regex.findall(diag[::-1])) for diag in ldown_diagonals])

n_xmas += sum([len(regex.findall(diag)) for diag in rdown_diagonals])
n_xmas += sum([len(regex.findall(diag[::-1])) for diag in rdown_diagonals])

print(n_xmas)

mas_regex = re.compile("MAS")
sam_regex = re.compile("SAM")

# match r_mas & inv_l_mas  + l_mas & inv_r_mas

rdown_masses = []
ldown_masses = []
for diag in rdown_diagonals:
    results = regex_match_all(mas_regex, diag)
    for result in results:
        if result is None:
            break
        for start, end in result.regs:
            xstart, xend = start - diag.count('_') + diag.count('-'), end - diag.count('_') + diag.count('-') - 1
            ystart, yend = start, end-1
            rdown_masses.append((xstart, ystart, xend, yend))
        results = mas_regex.search(diag, )

    results = regex_match_all(sam_regex, diag)
    for result in results:
        if result is None:
            break
        for end, start in result.regs:
            xstart, xend = start - diag.count('_') + diag.count('-') - 1, end - diag.count('_') + diag.count('-')
            ystart, yend = start - 1, end
            rdown_masses.append((xstart, ystart, xend, yend))

for diag in ldown_diagonals:
    results = regex_match_all(mas_regex, diag)
    for result in results:
        if result is None:
            break
        for start, end in result.regs:
            xstart, xend = len(diag) - 1 - start - diag.count('_') + diag.count('-'), len(diag) - 1 - (end-1) - diag.count('_') + diag.count('-')
            ystart, yend = start, end - 1
            ldown_masses.append((xstart, ystart, xend, yend))

    results = regex_match_all(sam_regex, diag)
    for result in results:
        if result is None:
            break
        for end, start in result.regs:
            xstart, xend = len(diag) - 1 - (start-1) - diag.count('_') + diag.count('-'), len(diag) - 1 - end - diag.count('_') + diag.count('-')
            ystart, yend = start - 1, end
            ldown_masses.append((xstart, ystart, xend, yend))

n_x_mas = 0
for possibility in rdown_masses:
    xstart, ystart, xend, yend = possibility
    if (xend, ystart, xstart, yend) in ldown_masses:
        n_x_mas += 1
    if (xstart, yend, xend, ystart) in ldown_masses:
        n_x_mas += 1

print(n_x_mas)

"""This would have been so much faster to implement:"""


# n_correct = 0
# for i in range(1, len(data)-1):
#     for j in range(1, len(data[i])-1):
#         if data[i][j] == 'A':
#             diag1 = data[i-1][j-1] + data[i][j] + data[i+1][j+1]
#             diag2 = data[i+1][j-1] + data[i][j] + data[i-1][j+1]
#             n_correct += diag1 in ['SAM', 'MAS'] and diag2 in ['SAM', 'MAS']
#
# print(n_correct)