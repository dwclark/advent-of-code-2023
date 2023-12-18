from aoc import non_blank_lines, print_assert
from BestCost import BestCost

def in_grid(grid, pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < len(grid) and pos[1] < len(grid[0])

def opposite(tup):
    return (tup[0] * -1, tup[1] * -1)

def next_to_add_p1(tups):
    ret = []
    current = tups[0]
    opp = opposite(current)
    for move in [(1,0),(-1,0),(0,1),(0,-1)]:
        if move != opp and tups.count(move) != 3:
            ret.append(move)
    return ret

def next_to_add_p2(tups):
    ret = []
    current = tups[0]
    opp = opposite(current)
    
    if tups[0:4].count(current) < 4:
        ret.append(current)
        return ret #if can't keep going, signal stop by returning empty

    for move in [(1,0),(-1,0),(0,1),(0,-1)]:
        if move != opp and tups.count(move) != 10:
            ret.append(move)
    return ret
    
def find_route(grid, next_to_add, num_to_track, start, goal):
    def next_states(state):
        ret = []
        pos = state[0]
        prev_moves = state[1:]

        for to_add in next_to_add(prev_moves):
            new_pos = (to_add[0] + pos[0], to_add[1] + pos[1])
            if in_grid(grid, new_pos):
                new_state = (new_pos, to_add) + prev_moves[0:num_to_track-1]
                ret.append(new_state)

        return ret
        
    best = BestCost()
    state = (start,) + tuple([(0,0) for i in range(0, num_to_track)])
    best.add(state, 0)

    while entry := best.get_next():
        cost, state = entry
        if state[0] == goal:
            return cost

        for ns in next_states(state):
            pos = ns[0]
            best.add(ns, cost + int(grid[pos[0]][pos[1]]))

grid = non_blank_lines('input/day17.txt')
start = (0,0)
goal = (len(grid)-1, len(grid[0])-1)

print_assert("Part 1:", find_route(grid, next_to_add_p1, 3, start, goal), 668)
print_assert("Part 2:", find_route(grid, next_to_add_p2, 10, start, goal), 788)
