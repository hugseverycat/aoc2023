"""
With thanks to https://arachnoid.com/area_irregular_polygon/index.html for how to calculate
the area of an irregular polygon by using its vertices
"""

with open('input/day18.txt') as f:
    lines = [line.rstrip() for line in f]

x = 0
y = 0
vertices = [(x, y)]
perimeter = 0
directions = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}

for line in lines:
    _, _, color = line.split()
    steps = int(color[2:7], 16)
    this_dir = int(color[7])
    if this_dir == 0:
        this_dir = 'R'
    elif this_dir == 1:
        this_dir = 'D'
    elif this_dir == 2:
        this_dir = 'L'
    else:
        this_dir = 'U'
    dx, dy = directions[this_dir]
    x += dx * steps
    y += dy * steps
    perimeter += steps
    vertices.append((x, y))

area = 0
ox, oy = vertices[0]
for x, y in vertices[1:]:
    area += (x * oy - y * ox)
    ox, oy = x, y
# I am not sure why I needed to add half the perimeter plus 1, but it gives the right answer!
area = abs(area // 2) + perimeter // 2 + 1
print(f"Part 2: {area}")
