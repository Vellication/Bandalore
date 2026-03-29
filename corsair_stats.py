"""Statistical analysis of Corsair trick distribution."""

from corsair import TRICK_RANKS, trick_check
from deck import full_deck
from itertools import combinations
import random


trick_distribution = {
    "Three Card Flush": 0,
    "Three Card Straight": 0,
    "Fraternal Three Of A Kind": 0,
    "Four Card Straight": 0,
    "Fraternal Four Of A Kind": 0,
    "Five Card Straight": 0,
    "Twain": 0,
    "Miser": 0,
    "Domain": 0,
    "Fraternal Five Of A Kind": 0,
    "Cleft": 0,
    "Pip Three Of A Kind": 0,
    "Unified Three Of A Kind": 0,
    "Union": 0,
    "Dominion": 0,
    "Dynasty": 0,
    None: 0
}

count = 0
while count < 250000:
    deck = full_deck[:]  # Create a copy
    random.shuffle(deck)
    hand = [deck.pop() for _ in range(3)]
    river = [deck.pop() for _ in range(5)]

    all_cards = hand + river

    # Find best trick that uses at least 1 from hand AND 1 from river
    best_trick = None
    best_score = 0

    for length in (3, 4, 5):
        for combo in combinations(all_cards, length):
            hand_count = sum(1 for card in combo if card in hand)
            river_count = sum(1 for card in combo if card in river)

            # Only consider combos that meet the constraint
            if hand_count > 0 and river_count > 0:
                trick_name = trick_check(combo)
                trick_score = TRICK_RANKS[trick_name]
                if trick_score > best_score:
                    best_score = trick_score
                    best_trick = trick_name

    # Only count if a valid trick was found
    if best_trick:
        trick_distribution[best_trick] += 1

    count += 1
    if count % 5000 == 0:
        print(f"Processed {count} hands")

print("\nTrick Distribution (best trick with hand + river constraint):")
for trick, cnt in sorted(trick_distribution.items(),
                         key=lambda x: x[1] if x[1] else 0, reverse=True):
    print(f"{trick}: {cnt}")