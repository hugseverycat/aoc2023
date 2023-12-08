from dataclasses import dataclass
from collections import deque


with open('input/day05.txt') as f:
    lines = [line.rstrip() for line in f]

@dataclass
class MapFilter:
    dest: range
    source: range


all_maps = []
seed_queue = deque()
seeds_input = True
temp_map = []
map_count = 0

for line in lines:  # Processing input
    if seeds_input:
        temp_seeds = [int(n) for n in line[7:].split()]
        seeds_input = False
        for i in range(len(temp_seeds)):
            if i % 2 != 0:
                seed_queue.append(range(temp_seeds[i - 1], temp_seeds[i - 1] + temp_seeds[i]))
    elif 'map' in line:  # Put the list of maps we just collected and add it to all_maps
        if map_count > 0:
            all_maps.append(temp_map)
            temp_map = []
        else:
            map_count += 1
    elif line == '':
        pass
    else:
        d, s, r = [int(i) for i in line.split()]
        # Storing each map as a destination range and a source range
        temp_map.append(MapFilter(range(d, d+r), range(s, s+r)))
all_maps.append(temp_map)  # collect the last set of maps

completed_seeds = []
map_counter = 0

for this_map_set in all_maps:
    print(f"Processing almanac {map_counter}...")
    map_counter += 1
    # Each seed in the queue that overlaps a map range will get split. Both seeds will be put back
    # in the queue. Once the seed is either entirely outside all ranges or entirely inside a single
    # range, it will be transformed if necessary and added to completed_seeds list
    while seed_queue:
        this_seed = seed_queue.pop()
        seed_transform = False
        for this_map in this_map_set:
            if this_seed.start < this_map.source.start and this_seed.stop - 1 in this_map.source:
                # If the seed starts below the map, and the last number in the seed (this_seed.stop-1)
                # is in the this_map.source range, then split the seed in 2 at this_map.source.start
                new_seed = range(this_seed.start, this_map.source.start)  # Last number not in range
                new_seed_2 = range(this_map.source.start, this_seed.stop)

                # Add the two new seeds back to the queue
                seed_queue.append(new_seed_2)
                seed_queue.append(new_seed)
                seed_transform = True
                break  # Stop checking additional maps; these seeds go back into the queue
            elif this_seed.start < this_map.source.start and this_seed.stop > this_map.source.stop:
                # If the seed starts below the map and ends above the map, then the seed range totally
                # encompasses this map range. It will be split into 3 seeds
                new_seed = range(this_seed.start, this_map.source.start)
                new_seed_2 = range(this_map.source.start, this_map.source.stop)
                new_seed_3 = range(this_map.source.stop, this_seed.stop)

                # Add all 3 seeds back to the queue
                seed_queue.append(new_seed)
                seed_queue.append(new_seed_2)
                seed_queue.append(new_seed_3)
                seed_transform = True
                break  # Stop checking this seed
            elif this_seed.start in this_map.source and this_seed.stop - 1 not in this_map.source:
                # If the seed start is inside the range and the last seed in the range (this_seed.stop-1)
                # is outside the range, then split the seed at the end of the map range.
                new_seed = range(this_seed.start, this_map.source.stop)
                new_seed_2 = range(this_map.source.stop, this_seed.stop)

                # Put seeds in queue
                seed_queue.append(new_seed)
                seed_queue.append(new_seed_2)
                seed_transform = True
                break
            elif this_seed.start >= this_map.source.start and this_seed.stop <= this_map.source.stop:
                # This seed is entirely within this map range
                # So we're going to transform it and put it in the completed_seeds list
                # Is this a bad assumption?? Should I check to see if it overlaps with other ranges?
                new_start = this_map.dest[this_map.source.index(this_seed.start)]
                new_stop = this_map.dest[this_map.source.index(this_seed.stop-1)]
                # Subtracting 1 since this_seed.stop-1 is not in the range

                this_seed = range(new_start, new_stop+1)  # Add 1 since the last number isn't in the range
                seed_transform = True
                completed_seeds.append(this_seed)
                break  # Stop checking; this seed is done!
            else:
                # Seed doesn't overlap at all so keep checking more maps
                pass
        # If checked all the maps without transforming or splitting this_seed (no breaks), then it is
        # completely outside any map ranges. Pass it to the completed_seeds list without changing it
        if not seed_transform:
            completed_seeds.append(this_seed)

    # We have passed all the seeds through all the maps in this almanac
    # Move all the completed seeds to the queue for the next round.
    for seed in completed_seeds:
        seed_queue.append(seed)
    completed_seeds = []

# We're done with all the almanacs so lets find the lowest location number
lowest = None
for seed in seed_queue:
    if lowest is None:
        lowest = seed.start
    else:
        if seed.start < lowest:
            lowest = seed.start

print(lowest)
