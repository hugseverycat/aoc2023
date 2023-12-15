import re
from dataclasses import dataclass

with open('input/day15.txt') as f:
    lines = [line.rstrip() for line in f]


@dataclass
class LensBox:
    number: int
    lens_labels: list
    focal_lengths: list


def run_hash(sequence: str):
    hash_value = 0
    for c in sequence:
        hash_value += ord(c)
        hash_value *= 17
        hash_value = hash_value % 256
    return hash_value


lens_boxes = dict()
verification_sum = 0
init_seq = lines[0].split(',')
for this_seq in init_seq:
    verification_sum += run_hash(this_seq)

for i in range(256):  # Generate our list of LensBoxes
    lens_boxes[i] = LensBox(i, [], [])

for counter, this_seq in enumerate(init_seq):
    label, focal_length = re.split('-|=', this_seq)
    box_num = run_hash(label)
    if '-' in this_seq:
        # Using a janky try-except to find out whether the label is already in the box
        try:
            remove_index = lens_boxes[box_num].lens_labels.index(label)
        except ValueError:
            # It's not in the box, do nothing
            pass
        else:
            # It's in the box, delete it and its focal length
            del lens_boxes[box_num].lens_labels[remove_index]
            del lens_boxes[box_num].focal_lengths[remove_index]
    elif '=' in this_seq:
        try:
            replace_index = lens_boxes[box_num].lens_labels.index(label)
        except ValueError:
            # It's not in the box, append it to the end of the list
            lens_boxes[box_num].lens_labels.append(label)
            lens_boxes[box_num].focal_lengths.append(int(focal_length))
        else:
            # A lens with this label is already in the box, replace it with new lens
            lens_boxes[box_num].lens_labels[replace_index] = label
            lens_boxes[box_num].focal_lengths[replace_index] = int(focal_length)

total_power = 0
for box in lens_boxes:
    for i, fl in enumerate(lens_boxes[box].focal_lengths):
        lens_power = (1 + box) * (i + 1) * fl
        total_power += lens_power

print(f"Part 1: {verification_sum}")
print(f"Part 2: {total_power}")
