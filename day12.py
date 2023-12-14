from aoc import non_blank_lines, print_assert

def keep_going(contents, groups, at):
    leftover = len(contents) - at
    needed = sum(groups) + len(groups) - 1
    return leftover >= needed

def can_place(contents, group, at):
    for i in range(at, at + group):
        if not contents[i] in [ '#', '?' ]:
            return False
        
    total = 0
    for i in range(0, at + group):
        if contents[i] == '#' or (i >= at and contents[i] == '?'):
            total = total + 1
    return (total == group) and (at + group == len(contents) or (at + group < len(contents) and contents[at + group] in [ '?', '.' ]))

def make_arrangements(contents, groups):
    made = []
    for at in range(0, len(contents)):
        if not keep_going(contents, groups, at):
            return made

        if can_place(contents, groups[0], at):
            first = contents[0:at] + ('#' * groups[0])
            
            if len(groups) > 1:
                rest = make_arrangements(contents[at + groups[0] + 1:], groups[1:])
                if rest:
                    made.extend([(first + '.' + item) for item in rest])
            elif contents.find('#', at + groups[0]) < 0:
                made.append(first + contents[at + groups[0]:])
    return made

def validate_arrangements(r, made):
    print(f"checking {r}")
    contents = r.contents
    groups = r.groups
    normalized = [ s.replace('?', '.') for s in made ]

    #check no double counting
    dedupe = set(normalized)
    assert len(dedupe) == len(normalized)

    #check all valid substitutions
    for m in made:
        assert len(m) == len(contents)
        for orig, new in zip(contents, m):
            assert orig == new or orig == '?'

    #check all groups are there and only they are there
    for m in normalized:
        index = 0
        for group_index, group in enumerate(groups):
            search = ('#' * group) + '.' if group_index + 1 < len(groups) else '#' * group
            index = m.find(search, index)
            if index < 0:
                assert index >= 0, f"1. bad generation {m} for {r}"
            index  = index + len(search)

        index = m.find('#', index)
        assert index < 0, f"2. bad generation {m} for {r}"
    
     
def arrangements(contents, groups):
    total = 0
    for at in range(0, len(contents)):
        if not keep_going(contents, groups, at):
            return total

        if can_place(contents, groups[0], at):
            if len(groups) > 1:
                total = total + 1 * arrangements(contents[at + groups[0] + 1:], groups[1:])
            elif contents.find('#', at + groups[0]) < 0:
                total = total + 1
    return total

class Record:
    def __init__(self, s):
        tmp = s.split(' ')
        self.contents = tmp[0]
        self.groups = [ int(sub) for sub in tmp[1].split(',') ]

    def __repr__(self):
        return f"{self.contents} {','.join([str(i) for i in self.groups])}"

def check_all(lines):
    for r in [Record(line) for line in lines]:
        made = make_arrangements(r.contents, r.groups)
        validate_arrangements(r, made)

def part_1(lines):
    return sum([arrangements(r.contents, r.groups) for r in [ Record(line) for line in lines ]])
    
lines = non_blank_lines('input/day12.txt')
