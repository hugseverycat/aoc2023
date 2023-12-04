import re

with open('input/day04.txt') as f:
    lines = [line.rstrip() for line in f]

total_score = 0
scratch_cards = dict()

for line in lines:
    winning_numbers, my_numbers = [n.strip() for n in line.split('|')]
    my_numbers = [int(n) for n in re.findall('\d+', my_numbers)]
    winning_numbers = [int(n) for n in re.findall('\d+', winning_numbers)]
    card_number, winning_numbers = winning_numbers[0], winning_numbers[1:]
    scratch_cards[card_number] = {'count': 1, 'wins': 0}

    # Find winning numbers and keep track of how many there are in the dictionary for this card
    for this_num in my_numbers:
        if this_num in winning_numbers:
            scratch_cards[card_number]['wins'] += 1

    total_score += int(2**(scratch_cards[card_number]['wins'] - 1))

# If this_card has i wins, and there are 'count' copies of this_card, then the next i cards get a new copy
# for each copy of this_card. So we'll add the 'count' of this_card to the count of the next i cards.
for this_card in scratch_cards:
    for i in range(scratch_cards[this_card]['wins']):
        scratch_cards[this_card + i + 1]['count'] += scratch_cards[this_card]['count']

total_cards = 0
for this_card in scratch_cards:
    total_cards += scratch_cards[this_card]['count']

print(f'Part 1: {total_score}')
print(f'Part 2: {total_cards}')
