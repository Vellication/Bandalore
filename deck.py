"""Corsair card deck definitions."""

# Constants
SUITS = ['O', 'G', 'P']
PIPS = list(range(1, 11))
FACES = {
    1: 'Wayfarer',
    2: 'Engineer',
    3: 'Scholar',
    4: 'Troubador',
    5: 'Merchant'
}
SPINS = ['↑', '↓']


class Card:
    """Parent class for all cards."""

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


class PipCard(Card):
    """Pip cards (numbered 1-10 in three suits)."""

    def __init__(self, pips, suit):
        super().__init__(pips, suit)

    def __str__(self):
        return f'{self.suit}{self.rank}'

    def __repr__(self):
        return f'PipCard({self.rank}, {self.suit})'


class FaceCard(Card):
    """Face cards (5 ranks × 3 suits × 2 spins = 30 total)."""

    def __init__(self, order, suit, spin):
        super().__init__(order, suit)
        self.spin = spin

    def to_roman(self, num):
        """Convert integer to Roman numeral."""
        vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX',
                'V', 'IV', 'I']
        result = ''
        for i, val in enumerate(vals):
            while num >= val:
                result += syms[i]
                num -= val
        return result

    def __str__(self):
        roman = self.to_roman(self.rank)
        return f'{self.suit} {self.spin}{roman}{self.spin}'

    def __repr__(self):
        return f'FaceCard({self.rank}, {self.suit}, {self.spin})'

    def get_kin_pips(self):
        """Return the two pip ranks that form twains/domains with this face.

        Kin pips are the two pips that sum to 11, where one matches the
        face rank (e.g., rank 3 has kin pips 3 and 8).
        """
        return (self.rank, 11 - self.rank)


# Generate all pip cards
pips_list = []
for suit in SUITS:
    for pips in PIPS:
        card = PipCard(pips, suit)
        pips_list.append(card)

# Generate all face cards
faces_list = []
for suit in SUITS:
    for rank, _ in FACES.items():
        for spin in SPINS:
            card = FaceCard(rank, suit, spin)
            faces_list.append(card)

# Full deck: all 60 cards
full_deck = []
full_deck.extend(pips_list)
full_deck.extend(faces_list)