from collections import deque

with open('input/day09.txt') as f:
    lines = [line.rstrip() for line in f]

oasis_values = []
for line in lines:
    oasis_values.append([int(n) for n in line.split()])

prediction_sum = 0
left_prediction_sum = 0
for this_value in oasis_values:
    zero_found = False
    addends = [deque([v for v in this_value])]
    counter = 0
    while not zero_found:
        seq_length = len(addends[counter])
        new_addends = deque()
        # Getting the difference between each number in the latest set of addends
        for i in range(1, seq_length):
            new_addends.append(addends[counter][i] - addends[counter][i-1])
        # Adding this new group of addends to the list
        addends.append(new_addends)
        counter += 1
        # Checking if all the new addends are the same
        if len(set(new_addends)) == 1:
            # Stop looping if they are
            zero_found = True

    total_a = len(addends)
    # Starting at the last list of addends, add the last number of this list
    # to the last number of the previous list to the end of the previous list
    # For part 2, subtract the first number of the previous from the first number
    # of the current list, then put that at the beginning of the previous list
    for i in range(total_a - 1, 0, -1):  # Iterate backwards
        addends[i - 1].append(addends[i][-1] + addends[i - 1][-1])
        addends[i - 1].appendleft(addends[i - 1][0] - addends[i][0])

    prediction_sum += addends[0][-1]
    left_prediction_sum += addends[0][0]

print(f"Part 1: {prediction_sum}")
print(f"Part 1: {left_prediction_sum}")
