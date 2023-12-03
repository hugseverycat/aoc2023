with open('input/day03.txt') as f:
    lines = [line.rstrip() for line in f]


def get_adjacents(number, location):
    # This function looks at a number and the (x, y) coords of its first digit and returns
    # a list of all (x, y) coords that are adjacent to the entire number
    nx, ny = location
    num_len = len(str(number))

    # Start the list of adjacents with the ones on the end
    # .x.....x.
    # .x12345x.
    # .x.....x.
    adjacents = [
        (nx - 1, ny - 1),
        (nx - 1, ny),
        (nx - 1, ny + 1),
        (nx + num_len, ny - 1),
        (nx + num_len, ny),
        (nx + num_len, ny + 1)
    ]

    for m in range(num_len):
        # Add the adjacents "above" and "below"
        adjacents.append((nx + m, ny - 1))
        adjacents.append((nx + m, ny + 1))

    return adjacents


part_numbers = dict()
symbols = dict()
part_number_sum = 0
gears = dict()  # For part 2
gear_ratio_sum = 0

y_coord = 0

for this_line in lines:
    # We will build the numbers digit by digit as a string
    current_number = ''
    x_coord = 0
    for this_char in this_line:
        # If we hit a digit, append it to current_number string
        if this_char.isdigit():
            current_number += this_char
        # If we hit something other than a digit
        else:
            if current_number.isdigit():
                # If we've currently got a number going, we've reached the end of the number.
                # Add the number to the dictionary. X will be its starting location, so we adjust
                # x_coord by the length of the number
                part_numbers[(x_coord - len(current_number), y_coord)] = int(current_number)
                current_number = ''  # Clear the current number
            if this_char != '.':
                # If it's a symbol, add it to the symbol dictionary
                symbols[(x_coord, y_coord)] = this_char
                # If it's a gear, add it to the gear dictionary (for part 2)
                if this_char == '*':
                    # Each entry in the gear dictionary is itself a dictionary. We'll increment
                    # n and g_ratio every time we encounter a part number adjacent to this gear
                    gears[(x_coord, y_coord)] = {'n': 0, 'g_ratio': 1}
        x_coord += 1
    if current_number.isdigit():
        # We're at the end of the line, so add current number to the dict if it exists
        part_numbers[(x_coord - len(current_number), y_coord)] = int(current_number)
        current_number = ''  # Clear the current number
    y_coord += 1

for part in part_numbers:
    # Get all the coordinates that are adjacent to this number
    part_adj = get_adjacents(part_numbers[part], part)

    # Check each adjacent location to see if a symbol is there
    for adj_loc in part_adj:
        if adj_loc in symbols:
            # Add the part number to the part number sum
            part_number_sum += part_numbers[part]

            # If the symbol is a gear, increment the number of adjacent parts for that gear
            # and increase its gear ratio
            if symbols[adj_loc] == '*':
                gears[adj_loc]['n'] += 1
                gears[adj_loc]['g_ratio'] *= part_numbers[part]
            break   # Break the for loop because we don't want to double-count any symbols

for gear in gears:
    # We are only concerned about gears with only 2 adjacent numbers
    if gears[gear]['n'] == 2:
        gear_ratio_sum += gears[gear]['g_ratio']

print(f'Part 1: {part_number_sum}')
print(f'Part 2: {gear_ratio_sum}')
