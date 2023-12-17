from collections import deque
with open('input/day16.txt') as f:
    lines = [line.rstrip() for line in f]

def display_board(m_dict: dict, a: set):
    for my in range(m_dict['max_y']):
        line = ''
        for mx in range(m_dict['max_x']):
            if (mx, my) in a:
                line += '☀️'
            else:
                line += '⬛'
        print(line)


mirrors = dict()
activated = set()
part1_activated = 0
mirrors['max_x'] = len(lines[0])
mirrors['max_y'] = len(lines)
beam_queue = deque()
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c != '.':
            mirrors[(x, y)] = c

beam_starts = []

for y in range(mirrors['max_y']):
    beam_starts.append((0, y, 1, 0))
    beam_starts.append((mirrors['max_x'] - 1, y, -1, 0))
for x in range(mirrors['max_x']):
    beam_starts.append((x, 0, 0, 1))
    beam_starts.append((x, mirrors['max_y'] - 1, 0, -1))


max_activated = 0
beam_states = []
total_starts = len(beam_starts)
for counter, beam_start in enumerate(beam_starts):
    if counter % 10 == 0:
        print(f"Checking state {counter} of {total_starts}")
    beam_queue.clear()
    beam_queue.append(beam_start)
    beam_states.clear()
    activated.clear()

    while beam_queue:
        this_beam = beam_queue.pop()
        lx, ly, dx, dy = this_beam
        while 0 <= lx < mirrors['max_x'] and 0 <= ly < mirrors['max_y'] and (lx, ly, dx, dy) not in beam_states:
            beam_states.append((lx, ly, dx, dy))
            activated.add((lx, ly))

            if (lx, ly) in mirrors:
                this_mirror = mirrors[(lx, ly)]
                if this_mirror == '\\':
                    dx, dy = dy, dx
                elif this_mirror == '/':
                    dx, dy = -dy, -dx
                elif this_mirror == '|' and abs(dx) == 1:
                    beam_queue.append((lx, ly, -dy, -dx))
                    dx, dy = dy, dx
                elif this_mirror == '-' and abs(dy) == 1:
                    beam_queue.append((lx, ly, -dy, -dx))
                    dx, dy = dy, dx
            lx += dx
            ly += dy
    if len(activated) > max_activated:
        max_activated = len(activated)
    if beam_start == (0, 0, 1, 0):
        part1_activated = len(activated)

print(f"Part 1: {part1_activated}")
print(f"Part 2: {max_activated}")
# Part 1: 6514
