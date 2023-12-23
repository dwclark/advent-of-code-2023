from aoc import non_blank_lines, print_assert
from collections import deque

def find_start(graph):
    for row_index, row in enumerate(graph):
        for col_index, col in enumerate(row):
            if col == 'S':
              ret = (row_index, col_index)
              graph[row_index] = row[0:col_index] + '.' + row[col_index+1:]
              return ret

def is_legal(graph, at):
    row, col = at
    return (row >= 0 and col >= 0 and row < len(graph)
            and col < len(graph[0]) and graph[row][col] != '#')

def total_reached(graph, start, num):
    q = deque()
    q.append((start, 0))
    reached = set()
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
        if steps == num:
            reached.add(pos)
        else:
            row, col = pos
            for next_pos in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
                if is_legal(graph, next_pos):
                    add_queue(next_pos, steps+1)

    return len(reached)

graph = non_blank_lines('input/day21.txt')
start = find_start(graph)
print(total_reached(graph, start, 64))
