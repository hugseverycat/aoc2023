import re

with open('input/day12.txt') as f:
    lines = [line.rstrip() for line in f]

spring_lines = []
for line in lines:
    spring_line, spring_groups = line.split()
    spring_groups = [int(f) for f in spring_groups.split(',')]
    spring_lines.append([spring_line, spring_groups])



def find_matches(test_str, blocks, position, block_num, block_len):
    current_state = (position, block_num, block_len)
    if current_state in saved_states:
        return saved_states[current_state]

    if position == len(test_str):
        # We don't have a set of blocks going
        # and the number of blocks we've completed is equal to the blocks we want to find
        # This is a valid solution
        if block_len == 0 and block_num == len(blocks):
            return 1
        # If we have a set of blocks going
        # Add to the blocknum because we've completed a block - compare to total blocks we want to find
        # And the length of this block has to be equal to the length of the corresponding block
        elif block_num + 1 == len(blocks) and block_len == blocks[block_num]:
            return 1
        # All other solutions are invalid
        else:
            return 0

    total_matches = 0
    if test_str[position] == '.':
        if block_len == 0:  # No block going
            total_matches += find_matches(test_str, blocks, position + 1, block_num, 0)
        elif block_len > 0 and block_num < len(blocks) and block_len == blocks[block_num]:
            # End this block, check for validity
            # If we don't have more blocks than the total number of blocks
            # and the length of the current block is equal to the corresponding block
            # then we are valid and can continue recursing. increase block number
            total_matches += find_matches(test_str, blocks, position + 1, block_num + 1, 0)
    elif test_str[position] == '#':
        # Increase the length of this block of broken springs
        total_matches += find_matches(test_str, blocks, position + 1, block_num, block_len + 1)
    elif test_str[position] == '?':
        # We're going to do all the stuff for '.' and '#' once each
        # First, pretend it's a '.'
        if block_len == 0:  # No block going
            total_matches += find_matches(test_str, blocks, position + 1, block_num, 0)
        elif block_len > 0 and block_num < len(blocks) and block_len == blocks[block_num]:
            # End this block, check for validity
            # If we don't have more blocks than the total number of blocks
            # and the length of the current block is equal to the corresponding block
            # then we are valid and can continue recursing. increase block number
            total_matches += find_matches(test_str, blocks, position + 1, block_num + 1, 0)
        # Then, pretend it's a #
        total_matches += find_matches(test_str, blocks, position + 1, block_num, block_len + 1)

    saved_states[current_state] = total_matches
    return total_matches


m = 0
for s in spring_lines:
    saved_states = {}
    matches = find_matches(s[0], s[1], 0, 0, 0)
    m += matches

print(f"Part 1: {m}")
for s in saved_states:
    print(f"{s}: {saved_states[s]}")
m = 0
'''for s in spring_lines:
    saved_states = {}
    sline = s[0]
    sline = (sline + '?')*5
    sline = sline[:-1]
    sgroup = s[1]*5
    matches = find_matches(sline, sgroup, 0, 0, 0)
    m += matches
print(f"Part 2: {m}")'''


# Correct P1: 7173
# Correct P2: 29826669191291