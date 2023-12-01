import regex as re
with open('input/day01.txt') as f:
    lines = [line.rstrip() for line in f]

part1 = False

total = 0
for line in lines:
    this_num = ''

    if part1:
        # Use regular expressions to find all the digits
        digits = re.findall("\d", line)
    else:
        # Use regular expressions to find all digits and all spelled-out numbers
        digits = re.findall("\d|one|two|three|four|five|six|seven|eight|nine", line, overlapped=True)

    if part1:
        # Put the first and last digit together in a string ('1' + '2' = '12')
        this_num = digits[0] + digits[-1]
    else:
        # Using the first and last items in the list of found numbers, convert words
        # into digits and put them together as a string ('1' + '2' = '12')
        for this_digit in [digits[0], digits[-1]]:
            if this_digit == 'one':
                this_num += '1'
            elif this_digit == 'two':
                this_num += '2'
            elif this_digit == 'three':
                this_num += '3'
            elif this_digit == 'four':
                this_num += '4'
            elif this_digit == 'five':
                this_num += '5'
            elif this_digit == 'six':
                this_num += '6'
            elif this_digit == 'seven':
                this_num += '7'
            elif this_digit == 'eight':
                this_num += '8'
            elif this_digit == 'nine':
                this_num += '9'
            else:
                this_num += this_digit

    # Turn the two digit string into a number and add it to the total
    total += int(this_num)

print(total)
