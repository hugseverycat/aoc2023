from dataclasses import dataclass

with open('input/day07.txt') as f:
    lines = [line.rstrip() for line in f]

RANK_ORDER = "AKQJT98765432"  # Part 1
RANK_ORDER = "AKQT98765432J"  # Part 2 -- comment me out to run part 1

class CamelHand:
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self.hand_type = self.get_type(self.cards)
        self.p2_type = self.get_p2_type(self.cards)

    def get_type(self, my_hand):
        each_card = set(my_hand)
        unique_cards = len(each_card)
        if unique_cards == 1:
            return 6  # 5 of a kind
        elif unique_cards == 2:
            for c in each_card:
                if my_hand.count(c) == 4:
                    return 5  # 4 of a kind
            return 4  # full house
        elif unique_cards == 3:
            for c in each_card:
                if my_hand.count(c) == 3:
                    return 3  # 3 of a kind
            return 2  # 2 pair
        elif unique_cards == 4:
            return 1  # pair
        else:
            return 0  # high card

    def get_p2_type(self, my_hand):
        joker_count = my_hand.count('J')
        best_hand = my_hand
        if joker_count == 0:
            return self.get_type(my_hand)

        no_jokers = my_hand.replace('J', '')
        each_card = set(no_jokers)
        for c in each_card:
            test_hand = no_jokers
            for _ in range(joker_count):
                test_hand += c
            if self.get_type(best_hand) < self.get_type(test_hand):
                best_hand = test_hand
        return self.get_type(best_hand)

    def is_stronger(self, compare_hand):
        if self.hand_type > compare_hand.hand_type:
            return True
        if self.hand_type < compare_hand.hand_type:
            return False
        for i, card in enumerate(self.cards):
            if RANK_ORDER.find(card) < RANK_ORDER.find(compare_hand.cards[i]):
                return True
            elif RANK_ORDER.find(card) > RANK_ORDER.find(compare_hand.cards[i]):
                return False
        return False

    def is_stronger_p2(self, compare_hand):
        if self.p2_type > compare_hand.p2_type:
            return True
        if self.p2_type < compare_hand.p2_type:
            return False
        for i, card in enumerate(self.cards):
            if RANK_ORDER.find(card) < RANK_ORDER.find(compare_hand.cards[i]):
                return True
            elif RANK_ORDER.find(card) > RANK_ORDER.find(compare_hand.cards[i]):
                return False
        return False


def sort_hands(h_list: list):  # Nasty bubble sort
    n = len(h_list)
    for ih in range(n):
        for j in range(0, n - ih - 1):
            #if h_list[j].is_stronger(h_list[j + 1]):  # Part 1 -- switch ifs to change parts
            if h_list[j].is_stronger_p2(h_list[j + 1]):  # Part 2
                h_list[j], h_list[j + 1] = h_list[j + 1], h_list[j]


hands = []
for line in lines:
    h, b = line.split()
    this_hand = CamelHand(h, int(b))
    hands.append(this_hand)

sort_hands(hands)
winnings = 0

for i, this_hand in enumerate(hands):
    winnings += this_hand.bid * (i + 1)

print(winnings)
