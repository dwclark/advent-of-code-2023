from aoc import non_blank_lines, print_assert

def my_hash(s):
    h = 0
    for c in s:
        h = h + ord(c)
        h = h * 17
        h = h % 256
    return h

def part_1(line):
    return sum([my_hash(c) for c in [ s for s in line.split(',') ] ])

def part_2(line):
    hash_list = []
    
    for num in range(0, 256):
        hash_list.append([])

    def remove(num, label):
        hash_list[num] = list([ tup for tup in hash_list[num] if tup[0] != label ])

    def modify(label, weight, tup):
        return (label, weight) if tup[0] == label else tup
    
    def add_modify(num, label, weight):
        my_list = hash_list[num]
        modified = False
        for index, tup in enumerate(my_list):
            if tup[0] == label:
                modified = True
                my_list[index] = (label, weight)
        if not modified:
            my_list.append((label, weight))
                
    for s in line.split(','):
        if s.count('-') == 1:
            label = s.replace('-', '')
            remove(my_hash(label), label)
        else:
            label, weight = s.split('=')
            add_modify(my_hash(label), label, int(weight))

    total = 0
    for outer_index,vals in enumerate(hash_list):
        for sub_index, tup in enumerate(vals):
            total = total + ((outer_index+1) * (sub_index+1) * tup[1])
    return total
        
line = non_blank_lines('input/day15.txt')[0]
print_assert("Part 1:", part_1(line), 506891)
print_assert("Part 2:", part_2(line), 230462)
