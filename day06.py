import math

with open('input/test.txt') as f:
    lines = [line.rstrip() for line in f]


def solve_quadratic(duration, record):
    a = -1
    record = -1 * record
    min_x = (-1 * duration + math.sqrt(duration * duration - 4 * a * record)) / (2 * a)
    max_x = (-1 * duration - math.sqrt(duration * duration - 4 * a * record)) / (2 * a)
    min_x = math.ceil(min_x)
    max_x = math.floor(max_x)
    return min_x, max_x


testing = False
part_one = False
record_value = 1

if testing:
    if part_one:
        races = [
            {'duration': 7,
             'record': 9},
            {'duration': 15,
             'record': 40},
            {'duration': 30,
             'record': 200}
        ]
    else:
        races = [{'duration': 71530, 'record': 940200}]
else:
    if part_one:
        races = [
            {'duration': 41,
             'record': 244},
            {'duration': 66,
             'record': 1047},
            {'duration': 72,
             'record': 1228},
            {'duration': 66,
             'record': 1040}
        ]
    else:
        races = [{'duration': 41667266, 'record': 244104712281040}]

for race in races:
    min_time, max_time = solve_quadratic(race['duration'], race['record'] + 1)
    ways_to_win = max_time - min_time + 1
    record_value *= ways_to_win

print(record_value)