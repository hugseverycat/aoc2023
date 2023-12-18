"""
The approach in this does not work for part 2; see day18-part2.py
In this one, we simply draw the border, then select an inside cell and use flood fill
"""

from collections import deque
with open('input/day18.txt') as f:
    lines = [line.rstrip() for line in f]

dig_plan = []
x = 0
y = 0

holes = {(x, y): None}
holes['max_x'] = x
holes['max_y'] = y
holes['min_x'] = x
holes['min_y'] = y
directions = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}

# Process input and fill out the edges of the trench
for line in lines:
    this_dir, steps, color = line.split()
    dx, dy = directions[this_dir]
    for i in range(int(steps)):
        x += dx
        y += dy
        holes[(x, y)] = color[1:-1]
        if x > holes['max_x']:
            holes['max_x'] = x
        if x < holes['min_x']:
            holes['min_x'] = x
        if y > holes['max_y']:
            holes['max_y'] = y
        if y < holes['min_y']:
            holes['min_y'] = y

# Find a suitable starting point
tx = holes['min_x']
ty = holes['min_y'] + (holes['max_y'] - holes['min_y'])//2
inside_start = None
while inside_start is None:
    for x in range(holes['min_x'], holes['max_x']):
        if (x, ty) in holes:
            if (x - 1, ty) not in holes and (x + 1, ty) not in holes:
                inside_start = (x + 1, ty)
                break
            else:
                ty += 1
                break

inside_holes = set()
inside_queue = deque()
inside_queue.append(inside_start)
while inside_queue:
    ix, iy = inside_queue.pop()
    for d in directions:
        dx, dy = directions[d]
        new_loc = (ix + dx, iy + dy)
        if new_loc not in holes and new_loc not in inside_holes:
            inside_queue.append(new_loc)
            inside_holes.add(new_loc)

print(f"Part 1: {len(inside_holes) + len(holes) - 4}")
