import re
from collections import deque
from math import lcm

with open('input/day08.txt') as f:
    lines = [line.rstrip() for line in f]

nodes = dict()  # Key will be node name e.g. 'AAA', value will be a tuple (L, R) e.g. ('BBB, 'CCC')
ghost_starts = []  # For part 2
ghost_ends = []

for i, line in enumerate(lines):
    if i == 0:
        directions = deque(line)  # Using a deque so we can rotate the list easily
    elif i == 1:
        pass
    else:
        c, l, r = re.findall('[A-Z0-9]+', line)
        nodes[c] = (l, r)
        if c[2] == 'A':
            ghost_starts.append(c)
        elif c[2] == 'Z':
            ghost_ends.append(c)

# List to store the number of steps it takes to get from each ghost start to the first ghost end
ghost_paths = []

# For each ghost start, follow the instructions til we reach a ghost end, then store that result
# in the ghost_paths list
for this_start in ghost_starts:
    current_node = this_start
    steps = 0
    while current_node[2] != 'Z':
        turn = directions[0]
        if turn == 'L':
            current_node = nodes[current_node][0]
        else:
            current_node = nodes[current_node][1]
        directions.rotate(-1)
        steps += 1
    ghost_paths.append(steps)
    if this_start == 'AAA':
        print(f"Part 1: {steps}")

# Find the least common multiple of the steps.
# This works because it turns out each A only goes to a single Z, and the loop repeats.
# The loop length is also a multiple of the number of steps.
print(f"Part 2: {lcm(*ghost_paths)}")
