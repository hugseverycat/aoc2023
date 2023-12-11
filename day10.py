from collections import deque

with open('input/day10.txt') as f:
    lines = [line.rstrip() for line in f]

tile_map = dict()
pipe_path = deque()
f_list = []


def get_neighbors(coord: tuple):
    gn_x, gn_y = coord
    return (gn_x, gn_y - 1), (gn_x, gn_y + 1), (gn_x - 1, gn_y), (gn_x + 1, gn_y)


# Returns the two coordinates (tuples) this pipe section connects to
# Returns None if there are no connections
def get_connections(coord: tuple, t_map: dict):
    cx, cy = coord
    if t_map[coord] == '|':
        return (cx, cy - 1), (cx, cy + 1)
    elif t_map[coord] == '-':
        return (cx + 1, cy), (cx - 1, cy)
    elif t_map[coord] == 'L':
        return (cx, cy - 1), (cx + 1, cy)
    elif t_map[coord] == 'J':
        return (cx - 1, cy), (cx, cy - 1)
    elif t_map[coord] == '7':
        return (cx - 1, cy), (cx, cy + 1)
    elif t_map[coord] == 'F':
        return (cx + 1, cy), (cx, cy + 1)
    else:
        return None


# Returns the next coordinate (tuple) in the pipe path
# Returns None if there are no connections
def get_next(coord: tuple, previous: tuple, t_map: dict):
    possible_nexts = get_connections(coord, t_map)
    if possible_nexts is None:
        return None
    elif possible_nexts[0] == previous:
        return possible_nexts[1]
    elif possible_nexts[1] == previous:
        return possible_nexts[0]
    else:
        pass


s_loc = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        tile_map[(x, y)] = c
        if c == 'S':
            curr_loc = (x, y)
            s_loc = curr_loc
            pipe_path.append(curr_loc)

starting_neighbors = get_neighbors(curr_loc)
starting_connections = None

for this_neighbor in starting_neighbors:
    nx, ny = this_neighbor
    connections = get_connections(this_neighbor, tile_map)
    if connections is not None:
        if curr_loc in connections:
            curr_loc = this_neighbor
            pipe_path.append(curr_loc)
            break  # Stop looking; we've found our first step

curr_loc = get_next(curr_loc, pipe_path[-2], tile_map)
while curr_loc is not None:
    pipe_path.append(curr_loc)
    curr_loc = get_next(curr_loc, pipe_path[-2], tile_map)


inside = False
insider_count = 0

pipe_path = set(pipe_path)
for y, line in enumerate(lines):
    for x, this_char in enumerate(line):
        check_coord = (x, y)
        if check_coord in pipe_path:
            if tile_map[check_coord] in 'LJ|':
                inside = not inside  # We've reached a boundary, toggle the inside boolean
        elif inside:
            insider_count += 1

print(f"Part 1: {len(pipe_path) // 2}")
print(f"Part 2: {insider_count}")
