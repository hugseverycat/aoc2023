with open('input/day11.txt') as f:
    lines = [line.rstrip() for line in f]


# Calculates the distance between two coordinates. Use the adjusted coordinates
# for each galaxy, not the original coordinates.
def manhattan_dist(coord_a: tuple, coord_b: tuple):
    ax, ay = coord_a
    bx, by = coord_b
    return abs(ax - bx) + abs(ay - by)


# Transforms the galaxy coordinate according to the lists of empty x and ys.
# The x and y lists must be ordered smallest to largest.
def adjust_galaxy(g_coord: tuple, x_adj_list: list, y_adj_list: list):
    gx, gy = g_coord
    x_adj = 0
    y_adj = 0

    # For both x and y, we'll find out how many empties are lower than the coord
    # and increase it by the adjustment factor (999999 for part 2) for each empty row
    # or column it is beyond
    for this_x in x_adj_list:
        if gx > this_x:
            x_adj += 999999
        else:
            break
    for this_y in y_adj_list:
        if gy > this_y:
            y_adj += 999999
        else:
            break
    return gx + x_adj, gy + y_adj


galaxies = dict()
galaxy_list = []
y_adjusts = []
x_adjusts = []
x_found = []

# Processing input. Going to store galaxies in a dictionary. The original location will be the key
# and the value will be its adjusted location (set to None initially)
for y, line in enumerate(lines):
    y_found = False  # Using this to see if there are any galaxies in this row
    for x, this_char in enumerate(line):
        try:
            # See if we already have an entry in x_found for this column
            _ = x_found[x]
        except IndexError:
            # If not, create it
            x_found.append(False)
        if this_char == '#':
            galaxies[(x, y)] = None
            galaxy_list.append((x, y))  # Using galaxy list to help loop through galaxies later on
            # We found a galaxy in this row and column
            y_found = True
            x_found[x] = True
    if not y_found:
        y_adjusts.append(y)  # y_adjusts keeps track of the original index of empty rows

# Go through x_found and populate the x_adjusts lists for empty columns
for x, _ in enumerate(lines[0]):
    if x_found[x] is not True:
        x_adjusts.append(x)

m_dist = 0

# Compare all the galaxies to all the other galaxies
for i in range(0, len(galaxy_list) - 1):
    this_galaxy = galaxy_list[i]
    if galaxies[this_galaxy] is None:  # Set adjusted coordinates for this galaxy
        galaxies[this_galaxy] = adjust_galaxy(this_galaxy, x_adjusts, y_adjusts)
    for j in range(i + 1, len(galaxy_list)):
        compare_galaxy = galaxy_list[j]
        if galaxies[compare_galaxy] is None:  # Set adjusted coordinates for this galaxy
            galaxies[compare_galaxy] = adjust_galaxy(compare_galaxy, x_adjusts, y_adjusts)
        # Note, we're sending the adjusted galaxy coordinates to the manhattan distance function
        m_dist += manhattan_dist(galaxies[this_galaxy], galaxies[compare_galaxy])

print(m_dist)
