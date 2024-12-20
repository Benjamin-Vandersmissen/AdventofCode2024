import re
from functools import lru_cache

data = open('day17').read().splitlines()
regex = re.compile('Register (?P<name>.): (?P<value>\d+)')

registers = {}
for line in data:
    match = regex.match(line)
    if match:
        registers[match.group('name')] = int(match.group('value'))
        continue
    else:
        if 'Program' in line:
            program = line[len('Program: '):].split(',')

def execute(program, registers):
    func_pointer = 0
    output = []
    while func_pointer < len(program):
        op = program[func_pointer]
        operand = program[func_pointer + 1]
        combo_operand = int(operand) if operand in ['0', '1', '2', '3', '7'] else registers[chr(ord('A') + int(operand) - 4)]

        match op:
            case '0':  # adv
                registers['A'] //= 2 ** combo_operand
            case '1':  # bxl
                registers['B'] = registers['B'] ^ int(operand)
            case '2':  # bst
                registers['B'] = combo_operand % 8
            case '3':  # jnz
                if registers['A']:
                    func_pointer = int(operand) - 2  # -2 , as such we can still increase func pointer at the end
            case '4':  # bxc
                registers['B'] = registers['B'] ^ registers['C']
            case '5':  # out
                output.append(combo_operand % 8)
            case '6':  # bdv
                registers['B'] = registers['A'] // (2 ** combo_operand)
            case '7':  # cdv
                registers['C'] = registers['A'] // (2 ** combo_operand)

        func_pointer += 2
    return output

print(','.join(map(str, execute(program, registers))))

@lru_cache(maxsize=None)
def reverse_engineer_program(depth = 0, factor = 0):
    possible_values = []
    for reg_a in range(factor * 8, factor * 8 + 8, 1):
        out = execute(program, {'A': reg_a, 'B': 0, 'C': 0})
        if out == list(map(int,program[-1-depth:])):
            possible_values.append(reg_a)
    return possible_values

factors = [(0, -1)]
while len(factors) > 0:
    factor, depth = factors.pop()
    if depth == len(program)-1:
        print(factor)
    factors += [(r, depth + 1) for r in reverse_engineer_program(depth =depth + 1, factor= factor)]
    factors = sorted(factors, key=lambda x: -(8 ** (len(program) - x[1]) + x[0]))