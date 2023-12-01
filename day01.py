from aoc import non_blank_lines, print_assert
import re

nums = {str(n): n for n in range(1,10)}
words = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
         'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
p1 = re.compile('([1-9])')
p2 = re.compile('(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))')

def solve(lines, p, d):
    def get_num(line):
        matches = re.findall(p, line)
        return 10 * d[matches[0]] + d[matches[-1]]
    return sum([get_num(line) for line in lines ])

lines = non_blank_lines('input/day01.txt')
print_assert("Part 1:", solve(lines, p1, nums), 54081)
print_assert("Part 2:", solve(lines, p2, nums | words), 54649)
