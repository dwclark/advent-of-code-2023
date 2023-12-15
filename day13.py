from aoc import blank_line_grouped, print_assert

class Grid:
    def __init__(self, lines):
        self.lines = lines

    def __repr__(self):
        return '\n'.join(self.lines) + '\n'

    def _horizontal(self, idx1, idx2):
        return all([s1 == s2 for s1, s2 in zip(self.lines[idx1], self.lines[idx2])])

    def _vertical(self, idx1, idx2):
        for line in self.lines:
            if line[idx1] != line[idx2]:
                return False
        return True

    def change_at(self, row, col):
        new_lines = list(self.lines)
        line = new_lines[row]
        new_val = '.' if line[col] == '#' else '#'
        new_line = line[0:col] + new_val + line[col+1:]
        assert line != new_line and len(new_line) == len(line), f"{row},{col} '{line}' '{new_line}'"
        new_lines[row] = new_line
        return Grid(new_lines)
    
    def horizontals(self):
        ret = []
        for row in range(0, len(self.lines)-1):
            if all([self._horizontal(lower, upper) for lower, upper in zip(range(row, -1, -1), range(row+1, len(self.lines)))]):
                ret.append(row+1)
        return ret

    def verticals(self):
        ret = []
        for col in range(0, len(self.lines[0])-1):
            if all([self._vertical(lower, upper) for lower, upper in zip(range(col, -1, -1), range(col+1, len(self.lines[0])))]):
                ret.append(col+1)
        return ret

def part_1(grids):
    horizontals = []
    verticals = []
    for g in grids:
        horizontals.extend(g.horizontals())
        verticals.extend(g.verticals())
        
    return sum([h * 100 for h in horizontals]) + sum([v for v in verticals])

def part_2(grids):
    horizontals = []
    verticals = []

    def find_new(i, g):
        prev_hs = g.horizontals()
        prev_vs = g.verticals()
        for row in range(0, len(g.lines)):
            for col in range(0, len(g.lines[0])):
                new_grid = g.change_at(row, col)
                new_hs = new_grid.horizontals()
                new_vs = new_grid.verticals()

                for new_h in new_hs:
                    if new_h not in prev_hs:
                        horizontals.append(new_h)
                        return

                for new_v in new_vs:
                    if new_v not in prev_vs:
                        verticals.append(new_v)
                        return
        assert False, f"should not be here {i} {g}"
            
    for i, g in enumerate(grids):
        find_new(i, g)
        
    return (sum(horizontals) * 100) + sum(verticals)

lines = blank_line_grouped('input/day13.txt')
grids = [Grid(line) for line in lines]

print_assert("Part 1:", part_1(grids), 29165)
print_assert("Part 2:", part_2(grids), 32192)
