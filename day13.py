with open('input/day13.txt') as f:
    lines = [line.rstrip() for line in f]

grid_list = []
new_grid = {}
y = 0
for this_line in lines:
    if this_line != '':
        if 'max_x' not in new_grid:
            new_grid['max_x'] = len(this_line) - 1
        for x, c in enumerate(this_line):
            if c == '#':
                new_grid[(x, y)] = '#'
        y += 1
    else:
        new_grid['max_y'] = y

        grid_list.append(new_grid)
        new_grid = {}
        y = 0
new_grid['max_y'] = y
grid_list.append(new_grid)


# A recursive function that checks for symmetry
# vert = True if checking for vertical symmetries
# sym_line = The line of symmetry we're checking. Should not change within the recursive function
# sym_len = The distance from the line of symmetry
# Basically we check points across the line of symmetry at distance sym_len and if they're
# the same, increase the distance and continue checking until we exceed the bounds of the grid. If we
# reach the edge of the grid, return True
# If we find a difference, return False
def find_symmetry(g: dict, vert: bool, sym_line: int, sym_len: int):
    my = g['max_y']
    mx = g['max_x']
    if vert:
        if sym_line + sym_len > mx or sym_line - sym_len <= 0:
            # We've exceeded the edge of the grid without finding a difference
            # so return True for this line of symmetry
            return True
        else:
            # Get the 2 x coordinates that are distance sym_len from the line we're checking
            cx1 = sym_line - sym_len - 1
            cx2 = sym_line + sym_len
            # Go down the column and look for differences
            for this_y in range(my + 1):
                # To maintain symmetry, they either have to both be # (and thus in the dictionary)
                # or both be . (and not in the dictionary
                if ((cx1, this_y) in g) is not ((cx2, this_y) in g):
                    # They're not the same, return False
                    return False
            # This column is symmetrical, increase the sym_len and continue checking
            return find_symmetry(g, vert, sym_line, sym_len + 1)
    else:
        # The logic is exactly the same except we're checking a horizontal line instead
        if sym_line + sym_len >= my or sym_line - sym_len <= 0:
            return True
        else:
            cy1 = sym_line - sym_len - 1
            cy2 = sym_line + sym_len
            for this_x in range(mx + 1):
                if ((this_x, cy1) in g) is not ((this_x, cy2) in g):
                    return False
            return find_symmetry(g, vert, sym_line, sym_len + 1)


# A recursive function that counts how many differences are along each line of symmetry
# If there's only 1 difference, then we've found the smudge.
# vert = True if checking vertical symmetries
# sym_line = The line of symmetry we're checking. Should not change within the recursive function
# sym_len = The distance from the line of symmetry
# We compare points across the line of symmetry just like the previous function, but instead of
# looking for perfect symmetry, we count the differences. If the differences exceed 1, we exit
# the recursion and return the differences. If we reach the edge of the grid, we return the
# difference. We'll check whether the difference is exactly equal to 1 outside the recursion
def find_smudge(g: dict, vert: bool, sym_line: int, sym_len: int):
    my = g['max_y']
    mx = g['max_x']
    if vert:
        # We've exceeded the bounds of the grid, and there are 0 differences out here
        if sym_line + sym_len > mx or sym_line - sym_len <= 0:
            return 0
        else:
            diff_counter = 0
            cx1 = sym_line - sym_len - 1
            cx2 = sym_line + sym_len
            for this_y in range(my + 1):
                if ((cx1, this_y) in g) is not ((cx2, this_y) in g):
                    # Count the differences
                    diff_counter += 1
            if diff_counter > 1:
                # We've already exceeded 1, no use continuing
                return diff_counter
            else:
                # We've found either 0 or 1 difference so far, so keep checking further out
                return diff_counter + find_smudge(g, vert, sym_line, sym_len + 1)
    else:
        # This is all exactly the same except checking horizontal lines of symmetry
        if sym_line + sym_len >= my or sym_line - sym_len <= 0:
            return 0
        else:
            diff_counter = 0
            cy1 = sym_line - sym_len - 1
            cy2 = sym_line + sym_len
            for this_x in range(mx + 1):
                if ((this_x, cy1) in g) is not ((this_x, cy2) in g):
                    diff_counter += 1
            if diff_counter > 1:
                return diff_counter
            else:
                return diff_counter + find_smudge(g, vert, sym_line, sym_len + 1)


# Part 1
vert_sum = 0
horiz_sum = 0
for this_grid in grid_list:
    vert_symmetry = False
    for x in range(1, this_grid['max_x'] + 1):
        vert_symmetry = find_symmetry(this_grid, True, x, 0)
        if vert_symmetry:
            vert_sum += x
            break
    if not vert_symmetry:
        for y in range(1, this_grid['max_y'] + 1):
            if find_symmetry(this_grid, False, y, 0):
                horiz_sum += y * 100
                break

print(f"Part 1: {vert_sum + horiz_sum}")

# Part 2
vert_sum = 0
horiz_sum = 0
for this_grid in grid_list:
    vert_found = False
    for x in range(1, this_grid['max_x'] + 1):
        vert_symmetry = find_smudge(this_grid, True, x, 0)
        if vert_symmetry == 1:
            vert_sum += x
            vert_found = True
            break
    if not vert_found:
        for y in range(1, this_grid['max_y'] + 1):
            horiz_symmetry = find_smudge(this_grid, False, y, 0)
            if horiz_symmetry == 1:
                horiz_sum += y * 100
                break

print(f"Part 2: {vert_sum + horiz_sum}")
