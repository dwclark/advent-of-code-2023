from aoc import non_blank_lines, print_assert

def split_and_convert(line):
    return [int(s) for s in line.split(' ') ]

def diffs(nums):
    new_list = []
    for i in range(0, len(nums)-1):
        new_list.append(nums[i+1] - nums[i])
    return new_list

def find_next(nums):
    if all([ n == 0 for n in nums]):
        return 0
    else:
        return nums[-1] + find_next(diffs(nums))

def find_first(nums):
    if all([ n == 0 for n in nums]):
        return 0
    else:
        return nums[0] - find_first(diffs(nums))

lines = non_blank_lines('input/day09.txt')
num_lines = [ split_and_convert(line) for line in lines ]

def part_1():
    return sum([find_next(num_line) for num_line in num_lines])

def part_2():
    return sum([find_first(num_line) for num_line in num_lines])
