from aoc import non_blank_lines, print_assert
import re

class Num:
    def __init__(self, line, start, end, num):
        self.line = line
        self.start = start
        self.end = end
        self.num = num
        self.symbols = {}

def make_nums(lines):
    p = re.compile(r"(\d+)")
    nums = []
    for index, line in enumerate(lines):
        for m in re.finditer(p, line):
            num = Num(index, m.start(), m.end(), int(line[m.start():m.end()]))
            nums.append(num)
    return nums

def find_symbol(num, lines):
    other = '0123456789.'
    for row in range(num.line-1, num.line+2):
        for col in range(num.start-1, num.end+1):
            if 0 <= row and 0 <= col and row < len(lines) and col < len(lines[0]) and not lines[row][col] in other:
                num.symbols[(row,col)] = lines[row][col]

def classify_nums(nums, lines):
    for num in nums:
        find_symbol(num, lines)
            
lines = non_blank_lines("input/day03.txt")
nums = make_nums(lines)
classify_nums(nums, lines)
print(sum([num.num for num in nums if len(num.symbols) > 0]))

lookup = {}
for num in nums:
    for coord, symbol in num.symbols.items():
        if symbol == '*':
            if coord in lookup:
                lookup[coord].append(num)
            else:
                lookup[coord] = [num]

print(sum([numlist[0].num * numlist[1].num for numlist in lookup.values() if len(numlist) == 2]))
        
    
