with open('input/day14.txt') as f:
    lines = [line.rstrip() for line in f]

def display_board(cols: int, rws: int, rnds: set, cbs: set):

    for y in range(rws):
        print_row = ''
        for x in range(cols):
            if (x, y) in rnds:
                print_row += '⚪'
            elif (x, y) in cbs:
                print_row += '🔳'
            else:
                print_row += '⬛'
        print(print_row)
    print()


def rotate_board(cols: int, rnds: set, cbs: set):
    new_rounds = set()
    new_cubes = set()
    for rock in rnds:
        rx, ry = rock
        new_rounds.add((cols - ry - 1, rx))
    for rock in cbs:
        rx, ry = rock
        new_cubes.add((cols - ry - 1, rx))
    return new_rounds, new_cubes

def tilt_board(cols: int, rnds: set, cbs: set):
    for cx in range(cols):
        move_rocks = set()
        move_start = 0
        for cy in range(cols):
            # We've found a round rock who could potentially move
            if (cx, cy) in rnds:
                move_rocks.add((cx, cy))
            # We've found a cube rock. Collect all the round rocks and move them
            # down as far as we can go, then reset everything and adjust move_start
            elif (cx, cy) in cbs:
                # Remove all the moving rocks from round_rocks; we will adjust them and re-add
                rnds = rnds.difference(move_rocks)
                for ci, _ in enumerate(move_rocks):
                    rnds.add((cx, move_start + ci))
                move_rocks.clear()
                move_start = cy + 1
            else:
                # I don't think I need to do anything about empty spaces...
                pass
        # Remove all the moving rocks from round_rocks; we will adjust them and re-add
        rnds = rnds.difference(move_rocks)
        for ci, _ in enumerate(move_rocks):
            rnds.add((cx, move_start + ci))
        move_rocks.clear()
    return rnds, cbs


def get_load(rws: int, rnds: set):
    load = 0
    for rock in rnds:
        rx, ry = rock
        load += rws - ry
    return load

# Process input
round_rocks = set()
cube_rocks = set()
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == 'O':
            round_rocks.add((x, y))
        elif c == '#':
            cube_rocks.add((x, y))

columns = len(lines[0])
rows = len(lines)

counter = 0
saved_states = dict()
load_list = []
repeat_state = None
cycle_start = 0

for counter in range(300):
    if counter % 10 == 0:
        print(counter)
    for t in range(4):
        round_rocks, cube_rocks = tilt_board(columns, round_rocks, cube_rocks)
        round_rocks, cube_rocks = rotate_board(columns, round_rocks, cube_rocks)

    load = get_load(columns, round_rocks)
    load_list.append(load)
    if tuple(round_rocks) in saved_states:
        if repeat_state is None:
            repeat_state = tuple(round_rocks)
            cycle_start = counter
            print(f"Cycle starting at {cycle_start}")
        elif tuple(round_rocks) == repeat_state:
            print(f"Cycle length is {counter - cycle_start}")
            cycle_length = counter - cycle_start
            final_load = cycle_start + (999999999 - cycle_start) % cycle_length
            print(f"Part 2: {load_list[final_load]}")
            break
    else:
        saved_states[tuple(round_rocks)] = load
