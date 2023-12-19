from dataclasses import dataclass
import re
from collections import deque

with open('input/day19.txt') as f:
    lines = [line.rstrip() for line in f]


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def cat(self, c):
        # This function takes a character c and returns the corresponding value
        if c == 'x':
            return self.x
        elif c == 'm':
            return self.m
        elif c == 'a':
            return self.a
        elif c == 's':
            return self.s

    def total_rating(self):
        # This function returns the total rating (for part 1)
        return self.x + self.m + self.a + self.s


@dataclass
class PartRange:
    x: range
    m: range
    a: range
    s: range

    def cat(self, c):
        # Takes a character c and returns the corresponding range
        if c == 'x':
            return self.x
        elif c == 'm':
            return self.m
        elif c == 'a':
            return self.a
        elif c == 's':
            return self.s

    def replace(self, c, r: range):
        # Takes the character c and range r and replaces the corresponding range with r
        if c == 'x':
            self.x = r
        elif c == 'm':
            self.m = r
        elif c == 'a':
            self.a = r
        elif c == 's':
            self.s = r

    def permutations(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

class Workflow:
    def __init__(self, flow_text: str):
        self.flows = flow_text.split(',')

    def __repr__(self):
        return str(self.flows)

    def analyze_workflow(self, pr: PartRange):
        # For part 2. For each workflow step, split the ranges into a part that will continue
        # with this workflow and a part that will go elsewhere. Parts that go elsewhere will
        # be stored in splits[]. Each item in splits[] is a list where the 1st item is the
        # string giving the workflow step to go to (or A or R), and the 2nd item is the PartRange
        splits = []
        for this_flow in self.flows:
            if '<' in this_flow or '>' in this_flow:  # Example: a<2006:qkq
                category = this_flow[0]  # in our example this is a
                compare_to = int(re.findall('\d+', this_flow)[0])  # example is 2006
                _, result = this_flow.split(':')  # result = qkq for the example
                cat_range = pr.cat(category)  # Should get the range for the 'a' category
                if '<' in this_flow:
                    if len(range(cat_range.start, compare_to)) > 0:  # If an overlap exists
                        new_range = PartRange(pr.x, pr.m, pr.a, pr.s)
                        # Replace the category range with the range that meets the criteria
                        new_range.replace(category, range(cat_range.start, compare_to))
                        # This new PartRange will go to splits
                        splits.append([result, new_range])
                        # Update pr (which is not going to splits yet) with the range that doesn't
                        # meet the criteria
                        pr.replace(category, range(compare_to, cat_range.stop))
                elif '>' in this_flow:
                    if len(range(compare_to, cat_range.stop)) > 0:
                        new_range = PartRange(pr.x, pr.m, pr.a, pr.s)

                        new_range.replace(category, range(compare_to + 1, cat_range.stop))
                        splits.append([result, new_range])

                        pr.replace(category, range(cat_range.start, compare_to + 1))
            else:
                # When we reach this code, we've got a range that just needs to go to a new workflow
                # or be accepted. this_flow should be just a string with the workflow ID, A, or R
                splits.append([this_flow, pr])
        return splits

    def do_workflow(self, p: Part):
        # Sends the part through this workflow and returns the next workflow (or A/R)
        for this_flow in self.flows:
            if '<' in this_flow or '>' in this_flow:
                category = this_flow[0]
                compare_to = int(re.findall('\d+', this_flow)[0])
                _, result = this_flow.split(':')
                if '<' in this_flow:
                    if p.cat(category) < compare_to:
                        return result
                elif '>' in this_flow:
                    if p.cat(category) > compare_to:
                        return result
            else:
                return this_flow


# Each part will be a Part object
parts = []

# Keys will be workflow name, value will be Workflow object
workflows = dict()

# Process input
toggle = True
for line in lines:
    if line == '':
        toggle = False
    elif toggle:
        # px{a<2006:qkq,m>2090:A,rfg}
        wf_name, wf_value = line.split('{')
        wf_value = wf_value[:-1]
        workflows[wf_name] = Workflow(wf_value)
    elif not toggle:
        # {x = 787, m = 2655, a = 1222, s = 2876}
        p_values = [int(v) for v in re.findall('\d+', line)]
        new_part = Part(*p_values)
        parts.append(new_part)

accepted = []
accepted_ranges = []

# Part 1
for this_part in parts:
    next_workflow = 'in'
    while next_workflow not in 'AR':
        next_workflow = workflows[next_workflow].do_workflow(this_part)
    if next_workflow == 'A':
        accepted.append(this_part)

rating = 0
for part in accepted:
    rating += part.total_rating()
print(f"Part 1: {rating}")

# Part 2
start_range = PartRange(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
# Queue will keep track of PartRanges we need to send through more workflows
# Each queue item will be a list where the first item is the workflow, and the 2nd is the PartRange
range_queue = deque([['in', start_range]])
while range_queue:
    test_workflow, test_range = range_queue.pop()
    range_splits = workflows[test_workflow].analyze_workflow(test_range)
    for r in range_splits:
        if r[0] == 'A':
            accepted_ranges.append(r[1])
        elif r[0] == 'R':
            continue
        else:
            range_queue.append(r)

total_possibilities = 0
for a in accepted_ranges:
    total_possibilities += a.permutations()

print(f"Part 2: {total_possibilities}")
