import numpy as np
import tqdm

with open('day7') as f:
    data  = f.read().split('\n')

def eval_left_to_right(operands, operators):
    cur_val = int(operands[0])
    for val, operator in zip(operands[1:], operators):
        if operator == '+':
            cur_val += int(val)
        elif operator == '*':
            cur_val *= int(val)
        elif operator == '|':
            cur_val = int(str(cur_val) + val)
    return cur_val

def can_produce_correct_result(result, operands):
    for i in range(2**(len(operands) - 1)):
        binary = np.binary_repr(i, len(operands)-1)
        operators = ['+' if c=='0' else '*' for c in binary]
        if eval_left_to_right(operands, operators) == int(result):
            return True
    return False

def can_produce_correct_result_concat(result, operands):
    for i in range(3**(len(operands) - 1)):
        ternary = np.base_repr(i, 3)
        ternary = (len(operands) - 1 - len(ternary))*'0' + ternary
        operator_map = {'0': '+', '1': '*', '2': '|'}
        operators = [operator_map[c] for c in ternary]
        if eval_left_to_right(operands, operators) == int(result):
            return True
    return False


return_value = 0

for row in tqdm.tqdm(data):
    result, operands = row.split(':')
    operands = operands.strip().split(' ')
    if can_produce_correct_result_concat(result, operands):
        return_value += int(result)

print(return_value)


