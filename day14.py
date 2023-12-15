"""
This code is trash

Basically I suck at detecting cycles and I gave up, so I just let it ran and watched the output
And then when I thought I had a cycle I did math to calculate the 1,000,000,000th cycle
It turned out that my input started a loop on 198 and it lasted 28 cycles. So
198 + (999999999 - 198) % 28 = 215. My answer was the 215th line of output.

For part 1 just run the tilt_board and the get_load functions.
"""

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
        # print(f"Checking column {x}")
        move_rocks = set()
        move_start = 0
        for cy in range(cols):
            # We've found a round rock who could potentially move
            if (cx, cy) in rnds:
                # print(f"Found round rock at {(x, y)}")
                move_rocks.add((cx, cy))
            # We've found a cube rock. Collect all the round rocks and move them
            # down as far as we can go, then reset everything and adjust move_start
            elif (cx, cy) in cbs:
                # print(f"Found cube rock at {(x, y)}. There are {len(move_rocks)} that can move down.")
                # Remove all the moving rocks from round_rocks; we will adjust them and re-add
                rnds = rnds.difference(move_rocks)
                for ci, _ in enumerate(move_rocks):
                    rnds.add((cx, move_start + ci))
                move_rocks.clear()
                move_start = cy + 1
            else:
                # I don't think I need to do anything about empty spaces...
                pass
        # print(f"Reached the end of this column. There are {len(move_rocks)} that can move down.")
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
results = set()
cycle = []
cycle_start = 0
cycle_repeat_start = 0
cycle_repeat_length = 0

#display_board(columns, rows, round_rocks, cube_rocks)

for counter in range(300):

    for t in range(4):
        round_rocks, cube_rocks = tilt_board(columns, round_rocks, cube_rocks)
        round_rocks, cube_rocks = rotate_board(columns, round_rocks, cube_rocks)
    #display_board(columns, rows, round_rocks, cube_rocks)

    load = get_load(columns, round_rocks)
    if (counter - 198) % 28 == 0 and counter > 198:
        print(f"Cycle repeat? Current load: {load}. Cycle start = {cycle[0]}")
    print(f"{counter}: {load}: {load in results}")
    if load in results:
        if len(cycle) == 0:
            print(f"  Starting new cycle at {counter}")
            cycle_start = counter
            cycle_start = 0
            cycle_repeat_length = 0
        else:
            if load == cycle[cycle_repeat_length]:
                if cycle_repeat_start == 0:
                    print(f"  Potential cycle repeat starting at {counter}")
                    cycle_repeat_start = counter
                    cycle_repeat_length = 0
                cycle_repeat_length += 1
            else:
                if cycle_repeat_start > 0:
                    print(f"  Cycle repeat broken at {counter}. Resetting to 0")
                cycle_repeat_start = 0
                cycle_repeat_length = 0
        cycle.append(load)
    else:
        cycle.clear()
        cycle_start = 0
    results.add(load)

#print(cycle)
#print(len(cycle))



# Part 1: 112046
# Part 2: 104639 (too high)
# Part 2: 104619 (correct)