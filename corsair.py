"""Corsair card game logic and trick evaluation."""

import random
from itertools import combinations

from deck import Card, PipCard, FaceCard, full_deck


# Trick rankings (0 = no trick, 1-16 = strength)
TRICK_RANKS = {
    "Three Card Flush": 1,
    "Three Card Straight": 2,
    "Fraternal Three Of A Kind": 3,
    "Four Card Straight": 4,
    "Fraternal Four Of A Kind": 5,
    "Five Card Straight": 6,
    "Twain": 7,
    "Miser": 8,
    "Domain": 9,
    "Fraternal Five Of A Kind": 10,
    "Cleft": 11,
    "Pip Three Of A Kind": 12,
    "Unified Three Of A Kind": 13,
    "Union": 14,
    "Dominion": 15,
    "Dynasty": 16,
    None: 0
}

TRICK_NAMES = {v: k for k, v in TRICK_RANKS.items()}

# Kin pips: the two pips that form twains/domains with each face rank
KIN_PIPS = {
    1: (1, 10),
    2: (2, 9),
    3: (3, 8),
    4: (4, 7),
    5: (5, 6)
}


# Card type utility functions
def all_faces(cards):
    """Check if all cards are face cards."""
    return all(isinstance(card, FaceCard) for card in cards)


def all_pips(cards):
    """Check if all cards are pip cards."""
    return all(isinstance(card, PipCard) for card in cards)


def get_face_cards(cards):
    """Filter and return only face cards from the list."""
    return [card for card in cards if isinstance(card, FaceCard)]


def get_pip_cards(cards):
    """Filter and return only pip cards from the list."""
    return [card for card in cards if isinstance(card, PipCard)]


def shares_suit(cards):
    """Check if all cards share the same suit."""
    suit = cards[0].suit
    return all(card.suit == suit for card in cards)


def shares_rank(cards):
    """Check if all cards share the same rank."""
    rank = cards[0].rank
    return all(card.rank == rank for card in cards)


def shares_spin(cards):
    """Check if all cards share the same spin."""
    spin = cards[0].spin
    return all(card.spin == spin for card in cards)


class Player:
    """Player in the game with hand, money, and betting state."""

    def __init__(self, hand=None, money=70, name='Player'):
        self.hand = hand if hand is not None else []
        self.money = money
        self.folded = False
        self.current_bet = 0
        self.name = name

    def fold(self):
        """Fold this player's hand."""
        self.folded = True

    def check(self, table_bet):
        """Player matches the current table bet."""
        amount_to_call = table_bet - self.current_bet
        if amount_to_call > self.money:
            print(f"{self.name} can't afford to check!")
            return False
        self.money -= amount_to_call
        self.current_bet += amount_to_call
        return True

    def raise_bet(self, amount, table_bet):
        """Player matches table bet and raises by amount."""
        total = (table_bet - self.current_bet) + amount
        if total > self.money:
            print(f"{self.name} can't afford to raise!")
            return False
        self.money -= total
        self.current_bet += total
        return True


class Dealer:
    """Dealer manages the deck and deals cards."""

    def __init__(self, deck=None):
        self.deck = deck if deck is not None else full_deck[:]

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.deck)

    def deal_to_players(self, player_list, cards_per_player=3):
        """Deal cards to each player."""
        for player in player_list:
            for _ in range(cards_per_player):
                player.hand.append(self.deck.pop())

    def deal_to_table(self, table, cards=5):
        """Deal cards to the table river."""
        for _ in range(cards):
            table.river.append(self.deck.pop())


class Table:
    """Table manages players, river cards, pot, and game phase."""

    def __init__(self, player_list, dealer=None, turn=0, phase=1):
        self.player_list = player_list
        self.dealer = dealer if dealer is not None else Dealer()
        self.turn = turn
        self.phase = phase
        self.river = []
        self.pot = 0

    def shuffle(self):
        """Shuffle the deck."""
        self.dealer.shuffle()

    def deal_hands(self, cards_per_player=3):
        """Deal hands to all players."""
        self.dealer.deal_to_players(self.player_list, cards_per_player)

    def deal_river(self, cards=5):
        """Deal river cards to the table."""
        self.dealer.deal_to_table(self, cards)


class Game:
    """Orchestrates a complete game."""

    def __init__(self, player_list):
        self.player_list = player_list
        self.dealer = Dealer()
        self.table = Table(player_list, self.dealer)

    def setup_round(self):
        """Initialize a new round: shuffle, deal hands, deal river."""
        self.table.shuffle()
        self.table.deal_hands()
        self.table.deal_river()

    def evaluate_hands(self):
        """Evaluate each player's best trick from hand + river."""
        results = {}
        for player in self.player_list:
            all_cards = player.hand + self.table.river
            best_trick = trick_check_iter(all_cards)
            results[player.name] = best_trick
        return results

    def play_round(self):
        """Play a complete round."""
        self.setup_round()
        results = self.evaluate_hands()
        return results

    def reset_round(self):
        """Reset the game for the next round."""
        for player in self.player_list:
            player.hand = []
        new_deck = full_deck[:]
        self.dealer.deck = new_deck
        self.table.river = []
        self.table.turn = 0

def is_flush(cards):
    """Check if three cards form a flush.

    All cards must share the same suit and be the same type
    (all faces or all pips).
    """
    return shares_suit(cards) and (all_faces(cards) or all_pips(cards))


def is_straight(cards):
    """Check if three cards form a straight (consecutive ranks)."""
    # Pips and faces can't form a straight together
    if not (all_faces(cards) or all_pips(cards)):
        return False

    ranks = [card.rank for card in cards]
    ranks.sort()
    return (ranks[1] == ranks[0] + 1 and
            ranks[2] == ranks[1] + 1)


def is_four_card_straight(cards):
    """Check if four cards form a straight (4 consecutive ranks)."""
    # Pips and faces can't form a straight together
    if not (all_faces(cards) or all_pips(cards)):
        return False

    ranks = [card.rank for card in cards]
    ranks.sort()
    return (ranks[1] == ranks[0] + 1 and
            ranks[2] == ranks[1] + 1 and
            ranks[3] == ranks[2] + 1)


def is_five_card_straight(cards):
    """Check if five cards form a straight (5 consecutive ranks)."""
    # Pips and faces can't form a straight together
    if not (all_faces(cards) or all_pips(cards)):
        return False

    ranks = [card.rank for card in cards]
    ranks.sort()
    return (ranks[1] == ranks[0] + 1 and
            ranks[2] == ranks[1] + 1 and
            ranks[3] == ranks[2] + 1 and
            ranks[4] == ranks[3] + 1)


def is_frat_three(cards):
    """Check if three cards form a fraternal three of a kind.

    Must be 3 faces with same rank and not all same spin.
    """
    # Must be all faces
    if not all_faces(cards):
        return False
    # Must not share spin
    spin = cards[0].spin
    if not all(card.spin == spin for card in cards):
        rank = cards[0].rank
        return all(card.rank == rank for card in cards)
    return False


def is_frat_four(cards):
    """Check if four cards form a fraternal four of a kind.

    Must be 4 faces with same rank and not all same spin.
    """
    # Must be all faces
    if not all_faces(cards):
        return False
    # Must not all share the same spin
    spin = cards[0].spin
    if not all(card.spin == spin for card in cards):
        rank = cards[0].rank
        return all(card.rank == rank for card in cards)
    return False


def is_frat_five(cards):
    """Check if five cards form a fraternal five of a kind.

    Must be 5 faces with same rank and not all same spin.
    """
    # Must be all faces
    if not all_faces(cards):
        return False
    # Must not all share the same spin
    spin = cards[0].spin
    if not all(card.spin == spin for card in cards):
        rank = cards[0].rank
        return all(card.rank == rank for card in cards)
    return False


def is_uni_three(cards):
    """Check if three cards form a unified three of a kind."""
    # Must be all faces
    if not all_faces(cards):
        return False
    # Must share spin
    spin = cards[0].spin
    if all(card.spin == spin for card in cards):
        rank = cards[0].rank
        return all(card.rank == rank for card in cards)
    return False


def is_pip_three(cards):
    """Check if three cards form a pip three of a kind."""
    # Cards must all be pips
    if not all_pips(cards):
        return False

    rank = cards[0].rank
    return all(card.rank == rank for card in cards)


def is_twain(cards):
    """Check if three cards form a twain.

    A twain is 1 face + 2 pips where one pip matches the face rank
    and two pips sum to 11.
    """
    # Separate face and pip cards
    face_cards = get_face_cards(cards)
    pip_cards = get_pip_cards(cards)

    # Must have exactly 1 face and 2 pips
    if len(face_cards) != 1 or len(pip_cards) != 2:
        return False

    face_card = face_cards[0]
    pip_ranks = [card.rank for card in pip_cards]

    # One pip must match the face rank
    if face_card.rank not in pip_ranks:
        return False

    # The two pips must sum to 11
    return sum(pip_ranks) == 11


def is_domain(cards):
    """Check if three cards form a domain (a suited twain).

    A domain is a twain where all cards share the same suit.
    Note: A domain is not a flush (it has mixed card types).
    """
    return is_twain(cards) and shares_suit(cards)


def is_miser(cards):
    """Check if four cards for a miser (1 face card and 3 kin pips)"""
    face_cards = get_face_cards(cards)
    pip_cards = get_pip_cards(cards)
     
    if len(face_cards) != 1 or len(pip_cards) != 3:
        return False
     
    kin_pips = face_cards[0].get_kin_pips()
    pip_ranks = sorted([card.rank for card in pip_cards])
     
    return all(kin in pip_ranks for kin in kin_pips)

def is_cleft(cards):
    """Check if four cards form a cleft (2 faced with different spins + kin pips).

    Two face cards of same rank with different spins, plus 2 pips that are
    kin to that rank (but not all same suit).
    """
    face_cards = get_face_cards(cards)
    pip_cards = get_pip_cards(cards)

    if len(face_cards) != 2 or len(pip_cards) != 2:
        return False

    test_list = pip_cards[:]
    test_list.append(face_cards[0])

    return ((is_twain(test_list) or is_domain(test_list)) and
            shares_rank(face_cards) and not shares_suit(face_cards))


def is_dominion(cards):
    """Check if four cards form a dominion (2 faced same suit + kin pips).

    Two face cards of same rank and same suit with different spins,
    plus 2 kin pips (all same suit).
    """
    face_cards = get_face_cards(cards)
    pip_cards = get_pip_cards(cards)

    if len(face_cards) != 2 or len(pip_cards) != 2:
        return False

    test_list = pip_cards[:]
    test_list.append(face_cards[0])

    return ((is_twain(test_list) or is_domain(test_list)) and
            shares_rank(face_cards) and shares_suit(face_cards) and
            not shares_spin(face_cards))


def is_union(cards):
    """Check if five cards form a union (fraternal 3 + 2 kin pips).

    Three face cards of same rank with different spins, plus 2 kin pips
    for that rank.
    """
    face_cards = get_face_cards(cards)
    pip_cards = get_pip_cards(cards)

    if len(face_cards) != 3 or len(pip_cards) != 2:
        return False

    # Check if the faces form a fraternal three
    if not is_frat_three(face_cards):
        return False

    # Check if the pips are kin to the face rank
    face_rank = face_cards[0].rank
    kin_pips = KIN_PIPS[face_rank]
    pip_ranks = sorted([card.rank for card in pip_cards])

    return all(kin in pip_ranks for kin in kin_pips)


def is_dynasty(cards):
    """Check if five cards form a dynasty (unified 3 + 2 kin pips).

    Three face cards of same rank with different spins, plus 2 kin pips
    for that rank.
    """
    face_cards = get_face_cards(cards)
    pip_cards = get_pip_cards(cards)

    if len(face_cards) != 3 or len(pip_cards) != 2:
        return False

    # Check if the faces form a unified three
    if not is_uni_three(face_cards):
        return False

    # Check if the pips are kin to the face rank
    face_rank = face_cards[0].rank
    kin_pips = KIN_PIPS[face_rank]
    pip_ranks = sorted([card.rank for card in pip_cards])

    return all(kin in pip_ranks for kin in kin_pips)


def trick_check(cards):
    """Check for the strongest trick formed by N cards (3, 4, or 5).

    Returns the name of the strongest trick, or None if no trick is found.
    """
    length = len(cards)

    if length == 3:
        if is_uni_three(cards):
            return "Unified Three Of A Kind"
        elif is_pip_three(cards):
            return "Pip Three Of A Kind"
        elif is_domain(cards):
            return "Domain"
        elif is_twain(cards):
            return "Twain"
        elif is_frat_three(cards):
            return "Fraternal Three Of A Kind"
        elif is_straight(cards):
            return "Three Card Straight"
        elif is_flush(cards):
            return "Three Card Flush"

    elif length == 4:
        if is_frat_four(cards):
            return "Fraternal Four Of A Kind"
        elif is_dominion(cards):
            return "Dominion"
        elif is_cleft(cards):
            return "Cleft"
        elif is_miser(cards):
            return "Miser"
        elif is_four_card_straight(cards):
            return "Four Card Straight"

    elif length == 5:
        if is_dynasty(cards):
            return "Dynasty"
        elif is_union(cards):
            return "Union"
        elif is_frat_five(cards):
            return "Fraternal Five Of A Kind"
        elif is_five_card_straight(cards):
            return "Five Card Straight"

    return None


def trick_check_iter(cards):
    """Find the strongest trick from any 3, 4, or 5-card combination.

    Checks all possible 3-card, 4-card, and 5-card combinations and returns
    the numeric rank (0-15) of the strongest trick found.
    Use TRICK_NAMES[result] to get the trick name if needed.
    """
    best_score = 0

    for length in (3, 4, 5):
        for combo in combinations(cards, length):
            current_score = TRICK_RANKS[trick_check(combo)]
            if current_score > best_score:
                best_score = current_score

    return best_score