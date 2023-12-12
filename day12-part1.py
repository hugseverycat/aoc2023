from dataclasses import dataclass
from collections import deque
import re

with open('input/day12.txt') as f:
    lines = [line.rstrip() for line in f]

# ???.### 1,1,3
# ????.######..#####. 1,6,5

@dataclass
class SpringLines:
    line: str
    groups: tuple

# Return 'possible' if it is possible but not complete
# Return 'complete' if it is a complete match
# Return 'fail' if it cannot match
def is_possible(test_str: str, spr_groups):
    # #??.### 1,1,3
    if '?' in test_str:
        first_part = test_str.split('?')[0]
        damaged_groups = tuple([len(r) for r in re.findall('(#+)\.', first_part)])
    else:
        first_part = test_str
        damaged_groups = tuple([len(r) for r in re.findall('#+', first_part)])
    if damaged_groups == spr_groups and '?' not in test_str:
        #print(f"{test_str} is a match for {spring.line}. {damaged_groups} == {spring.groups}")
        return 'complete'
    for i, this_group in enumerate(damaged_groups):
        try:
            if this_group != spr_groups[i]:
                '''print(f"{test_str} failed because {first_part} with groups {damaged_groups} "
                      f"doesn't match {spring.groups} at index {i}")'''
                return 'fail'
        except IndexError:
            return ('fail')
    #print(f"{test_str} is a possible match for {spring_line}. {damaged_groups} compatible with {spring.groups}")
    return 'possible'

def replace_first(spring_str: str):
    op_replace = spring_str.replace('?', '.', 1)
    dam_replace = spring_str.replace('?', '#', 1)
    return op_replace, dam_replace


def get_matches(spring: SpringLines):
    possibles = deque()
    matches = []
    p1, p2 = replace_first(spring.line)
    possibles.append(p1)
    possibles.append(p2)
    while possibles:
        test_spring = possibles.pop()
        if '?' in test_spring:
            # print(f"Testing possible: {test_spring}")
            p1, p2 = replace_first(test_spring)
            p1_test = is_possible(p1, spring.groups)
            p2_test = is_possible(p2, spring.groups)
            if p1_test == 'possible':
                possibles.append(p1)
            elif p1_test == 'complete':
                matches.append(p1)
            if p2_test == 'possible':
                possibles.append(p2)
            elif p2_test == 'complete':
                matches.append(p2)
    return matches


spring_list = []
match_list = []
total_matches = 0

for line in lines:
    spring_line, spring_groups = line.split()
    spring_groups = tuple([int(f) for f in spring_groups.split(',')])
    spring_list.append(SpringLines(spring_line, spring_groups))

for spring in spring_list:
    spring_matches = get_matches(spring)
    total_matches += len(spring_matches)
    match_list.append(spring_matches)

print(f"Part 1: {total_matches}")

# 7409 too high
# Part 1: 7173
