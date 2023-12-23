from aoc import non_blank_lines, print_assert
from collections import deque

def find_start(graph):
    for row_index, row in enumerate(graph):
        for col_index, col in enumerate(row):
            if col == 'S':
              ret = (row_index, col_index)
              graph[row_index] = row[0:col_index] + '.' + row[col_index+1:]
              return ret

def is_legal_1(graph, at):
    row, col = at
    return (row >= 0 and col >= 0 and row < len(graph)
            and col < len(graph[0]) and graph[row][col] != '#')

def is_legal_2(graph, at):
    raw_row, raw_col = at
    row = raw_row % len(graph)
    col = raw_col % len(graph)
    return graph[row][col] != '#'

def total_reached(graph, start, num, is_legal):
    q = deque()
    q.append((start, 0))
    cache = {}
    
    def add_queue(pos, steps):
        sub = cache.get(steps)
        if not sub:
            sub = set()
            cache[steps] = sub

        if not pos in sub:
            sub.add(pos)
            q.append((pos, steps))
    
    while q:
        pos, steps = q.popleft()
        if steps > num:
            break
        else:
            row, col = pos
            for next_pos in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
                if is_legal(graph, next_pos):
                    add_queue(next_pos, steps+1)

    return { n:len(c) for n, c in cache.items() }

def part_2(graph, start, num):
    remainder = num % len(graph)
    days_map = total_reached(graph, start, remainder + (2 * len(graph)), is_legal_2)

    v1 = days_map[remainder]
    v2 = days_map[remainder + len(graph)]
    v3 = days_map[remainder + (2 * len(graph))]

    a = (v1 - 2*v2 + v3) / 2
    b = (-3*v1 + 4*v2 - v3) / 2
    c = v1
    n = int(num / len(graph))
    return int((a * n * n) + (b * n) + c)
    
graph = non_blank_lines('input/day21.txt')
start = find_start(graph)
print_assert("Part 1:", total_reached(graph, start, 64, is_legal_1)[64], 3600)
print_assert("Part 2:", part_2(graph, start, 26501365), 599763113936220)
