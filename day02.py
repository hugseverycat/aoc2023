with open('input/day02.txt') as f:
    lines = [line.rstrip() for line in f]

game_id = 1
id_sum = 0
cube_power = 0

blue_limit = 14
red_limit = 12
green_limit = 13

for line in lines:
    max_blue, max_red, max_green = 0, 0, 0
    # Split out the game numbering from the actual draws
    _, cubes = line.split(':')

    # Split by each draw
    grabs = cubes.split(';')

    for this_grab in grabs:
        # Split by color
        grabbed_cubes = [g.strip() for g in this_grab.split(',')]
        for cube_set in grabbed_cubes:
            n, color = cube_set.split(' ')
            # Find how many of each color were drawn and compare against the maximum drawn so far
            if color == 'blue':
                if int(n) > max_blue:
                    max_blue = int(n)
            elif color == 'red':
                if int(n) > max_red:
                    max_red = int(n)
            elif color == 'green':
                if int(n) > max_green:
                    max_green = int(n)

    # Find possible games for part 1 and increment game id
    if max_blue <= blue_limit and max_red <= red_limit and max_green <= green_limit:
        id_sum += game_id
    game_id += 1

    # Calculate power for part 2
    this_power = max_blue * max_red * max_green
    cube_power += this_power

print(f'Part 1: {id_sum}')
print(f'Part 2: {cube_power}')
