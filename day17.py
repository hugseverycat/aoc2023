"""
With thanks to reddit user u/bakibol whose solution helped me figure this out
https://www.reddit.com/r/adventofcode/comments/18k9ne5/comment/kdsi78i
"""

from heapq import heappop, heappush
from collections import defaultdict

with open('input/day17.txt') as f:
    lines = [line.rstrip() for line in f]

max_x = len(lines[0]) - 1
max_y = len(lines) - 1

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
max_straight = 10  # Set to 3 for part 1, 10 for part 2
min_straight = 4  # Set to 0 for part 1, 4 for part 2


def get_possible_neighbors(curr_loc, curr_dir, str_count):
    clx, cly = curr_loc
    cdx, cdy = curr_dir
    neighbor_list = []
    # If we're just starting out, we don't have a direction so we'll just return the 2
    # locations we already know are valid
    if curr_loc == (0, 0) and curr_dir == (0, 0):
        return [(1, 0), (0, 1)]
    for d in directions:
        dx, dy = d
        if (dx, dy) == (-cdx, -cdy):
            # If this is backwards, do not add
            continue
        if (dx, dy) == (cdx, cdy) and str_count == max_straight:
            # If this is straight, and we've reached the maximum, do not add
            continue
        if str_count < min_straight and (dx, dy) != (cdx, cdy):
            # If we haven't reached the minimum straight, and this is not straight, don't add
            continue
        if (clx + dx, cly + dy) in heat_map:
            # If we haven't bailed yet, and the coordinate exists, add it
            neighbor_list.append((clx + dx, cly + dy))
    return neighbor_list


heat_map = dict()

for y, this_row in enumerate(lines):
    for x, heat in enumerate(this_row):
        heat_map[(x, y)] = int(heat)

start = (0, 0)
heat_queue = [(0, start, (0, 0), 1)]
distances = defaultdict(lambda: defaultdict(lambda: float("inf")))

while heat_queue:
    # Put heat_loss first so that the heapq will order the heap by this
    heat_loss, (cx, cy), (dx, dy), straight = heappop(heat_queue)
    neighbors = get_possible_neighbors((cx, cy), (dx, dy), straight)
    for n in neighbors:
        nx, ny = n

        # Subtract to derive new direction of movement
        ndx = nx - cx
        ndy = ny - cy
        if (ndx, ndy) == (dx, dy):  # Going straight
            new_straight = straight + 1
        else:
            new_straight = 1  # Not going straight, reset
        new_heat_loss = heat_loss + heat_map[n]

        # If the heat loss here is less than the heat loss from the last path we tried
        # that went through this location in this direction with this straight count,
        # then add it to the queue to be processed
        if new_heat_loss < distances[n][(ndx, ndy), new_straight]:
            distances[n][(ndx, ndy), new_straight] = new_heat_loss
            heappush(heat_queue, (new_heat_loss, n, (ndx, ndy), new_straight))

print(min(distances[(max_x, max_y)].values()))
