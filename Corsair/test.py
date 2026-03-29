"""Test suite for Corsair trick evaluation functions."""

import sys

from deck import PipCard, FaceCard
from corsair import (
    is_flush, is_straight, is_frat_three, is_uni_three,
    is_domain, is_twain, is_pip_three, is_frat_four,
    is_four_card_straight, is_miser, is_cleft, is_dominion,
    is_frat_five, is_five_card_straight, is_union, is_dynasty
)


def test_is_flush():
    """Test flush detection."""
    print("Testing is_flush...")
    # All same suit, all pips
    assert is_flush([PipCard(1, 'O'), PipCard(5, 'O'), PipCard(10, 'O')])
    # Mixed suits (should fail)
    assert not is_flush([PipCard(1, 'O'), PipCard(5, 'G'), PipCard(10, 'P')])
    # Face cards same suit
    assert is_flush([FaceCard(1, 'G', '↑'), FaceCard(2, 'G', '↓'),
                     FaceCard(3, 'G', '↑')])
    # Mixed card types, same suit (should fail - not all same type)
    assert not is_flush([PipCard(5, 'P'), FaceCard(3, 'P', '↑'),
                         PipCard(9, 'P')])
    print("✓ is_flush passed")


def test_is_straight():
    """Test straight detection."""
    print("Testing is_straight...")
    # Valid straight (pips)
    assert is_straight([PipCard(1, 'O'), PipCard(2, 'O'), PipCard(3, 'O')])
    # Unsorted straight (pips)
    assert is_straight([PipCard(5, 'G'), PipCard(3, 'G'), PipCard(4, 'G')])
    # Not consecutive (pips)
    assert not is_straight([PipCard(1, 'O'), PipCard(2, 'O'),
                            PipCard(4, 'O')])
    # Valid straight (faces)
    assert is_straight([FaceCard(1, 'P', '↑'), FaceCard(2, 'P', '↓'),
                        FaceCard(3, 'P', '↑')])
    # Mixed types (should fail)
    assert not is_straight([PipCard(1, 'O'), FaceCard(2, 'O', '↑'),
                            PipCard(3, 'O')])
    print("✓ is_straight passed")


def test_is_frat_three():
    """Test fraternal three of a kind detection."""
    print("Testing is_frat_three...")
    # Same rank, different spins
    assert is_frat_three([FaceCard(2, 'O', '↑'), FaceCard(2, 'G', '↓'),
                          FaceCard(2, 'P', '↑')])
    # Same rank, same spin (should fail)
    assert not is_frat_three([FaceCard(3, 'O', '↑'), FaceCard(3, 'G', '↑'),
                              FaceCard(3, 'P', '↑')])
    # With pips (should fail)
    assert not is_frat_three([PipCard(2, 'O'), FaceCard(2, 'G', '↓'),
                              FaceCard(2, 'P', '↑')])
    print("✓ is_frat_three passed")


def test_is_uni_three():
    """Test unified three of a kind detection."""
    print("Testing is_uni_three...")
    # Same rank, same spin
    assert is_uni_three([FaceCard(4, 'O', '↓'), FaceCard(4, 'G', '↓'),
                         FaceCard(4, 'P', '↓')])
    # Same rank, different spins (should fail)
    assert not is_uni_three([FaceCard(1, 'O', '↑'), FaceCard(1, 'G', '↓'),
                             FaceCard(1, 'P', '↑')])
    # With pips (should fail)
    assert not is_uni_three([PipCard(4, 'O'), FaceCard(4, 'G', '↓'),
                             FaceCard(4, 'P', '↓')])
    print("✓ is_uni_three passed")


def test_is_pip_three():
    """Test pip three of a kind detection."""
    print("Testing is_pip_three...")
    # Same pip rank
    assert is_pip_three([PipCard(5, 'O'), PipCard(5, 'G'), PipCard(5, 'P')])
    # Different pip ranks (should fail)
    assert not is_pip_three([PipCard(3, 'O'), PipCard(5, 'G'),
                             PipCard(7, 'P')])
    # With face cards (should fail)
    assert not is_pip_three([PipCard(2, 'O'), PipCard(2, 'G'),
                             FaceCard(2, 'P', '↑')])
    print("✓ is_pip_three passed")


def test_is_domain():
    """Test domain detection."""
    print("Testing is_domain...")
    # Valid domain: Twain that's also a flush (all same suit)
    assert is_domain([FaceCard(1, 'O', '↑'), PipCard(1, 'O'),
                      PipCard(10, 'O')])
    # Valid domain: Face(3), Pip(3), Pip(8) all same suit
    assert is_domain([FaceCard(3, 'G', '↓'), PipCard(3, 'G'),
                      PipCard(8, 'G')])
    # Invalid: not a twain (pips don't sum to 11)
    assert not is_domain([FaceCard(1, 'O', '↑'), PipCard(1, 'O'),
                          PipCard(9, 'O')])
    # Invalid: not a twain (no pip matches face rank)
    assert not is_domain([FaceCard(2, 'O', '↑'), PipCard(1, 'O'),
                          PipCard(10, 'O')])
    # Invalid: is twain but not a flush (different suits)
    assert not is_domain([FaceCard(1, 'O', '↑'), PipCard(1, 'G'),
                          PipCard(10, 'P')])
    print("✓ is_domain passed")


def test_is_twain():
    """Test twain detection."""
    print("Testing is_twain...")
    # Valid twain: 1 face + 2 pips, one matches rank, sum to 11
    assert is_twain([FaceCard(1, 'O', '↑'), PipCard(1, 'G'),
                     PipCard(10, 'P')])
    # Valid twain: different suits
    assert is_twain([FaceCard(1, 'O', '↑'), PipCard(1, 'G'),
                     PipCard(10, 'P')])
    # Invalid: pips don't sum to 11
    assert not is_twain([FaceCard(1, 'O', '↑'), PipCard(1, 'G'),
                         PipCard(9, 'P')])
    # Invalid: no pip matches face rank
    assert not is_twain([FaceCard(2, 'O', '↑'), PipCard(1, 'G'),
                         PipCard(10, 'P')])
    print("✓ is_twain passed")


def test_is_frat_four():
    """Test fraternal four of a kind detection."""
    print("Testing is_frat_four...")
    # 4 faces, same rank, different spins
    assert is_frat_four([FaceCard(3, 'O', '↑'), FaceCard(3, 'G', '↓'),
                         FaceCard(3, 'P', '↑'), FaceCard(3, 'O', '↓')])
    # All same spin (should fail)
    assert not is_frat_four([FaceCard(1, 'O', '↑'), FaceCard(1, 'G', '↑'),
                             FaceCard(1, 'P', '↑'), FaceCard(1, 'O', '↑')])
    print("✓ is_frat_four passed")


def test_is_miser():
    """Test miser detection."""
    print("Testing is_miser...")
    # 1 face + 3 kin pips
    assert is_miser([FaceCard(4, 'O', '↑'), PipCard(4, 'G'), PipCard(7, 'P'),
                     PipCard(4, 'O')])
    # Invalid: wrong pips
    assert not is_miser([FaceCard(4, 'O', '↑'), PipCard(4, 'G'), PipCard(6, 'P'),
                         PipCard(5, 'O')])
    print("✓ is_miser passed")


def test_is_cleft():
    """Test cleft detection."""
    print("Testing cleft...")
    # 2 faces same rank, different spins, not same suit + kin pips
    assert is_cleft([FaceCard(2, 'O', '↑'), FaceCard(2, 'G', '↓'),
                     PipCard(2, 'P'), PipCard(9, 'O')])
    print("✓ is_cleft passed")


def test_is_dominion():
    """Test dominion detection."""
    print("Testing is_dominion...")
    # 2 faces same rank, same suit, different spins + kin pips all same suit
    assert is_dominion([FaceCard(1, 'O', '↑'), FaceCard(1, 'O', '↓'),
                        PipCard(1, 'O'), PipCard(10, 'O')])
    print("✓ is_dominion passed")


def test_is_union():
    """Test union detection."""
    print("Testing is_union...")
    # 3 fraternal faces + 2 kin pips
    assert is_union([FaceCard(5, 'O', '↑'), FaceCard(5, 'G', '↓'),
                     FaceCard(5, 'P', '↑'), PipCard(5, 'O'), PipCard(6, 'G')])
    print("✓ is_union passed")


def test_is_dynasty():
    """Test dynasty detection."""
    print("Testing is_dynasty...")
    # 3 unified faces + 2 kin pips
    assert is_dynasty([FaceCard(2, 'O', '↓'), FaceCard(2, 'G', '↓'),
                       FaceCard(2, 'P', '↓'), PipCard(2, 'O'), PipCard(9, 'G')])
    # Invalid: not unified (different spins)
    assert not is_dynasty([FaceCard(1, 'O', '↑'), FaceCard(1, 'G', '↓'),
                           FaceCard(1, 'P', '↑'), PipCard(1, 'O'), PipCard(10, 'G')])
    print("✓ is_dynasty passed")


if __name__ == '__main__':
    try:
        test_is_flush()
        test_is_straight()
        test_is_frat_three()
        test_is_uni_three()
        test_is_pip_three()
        test_is_domain()
        test_is_twain()
        test_is_frat_four()
        test_is_miser()
        test_is_cleft()
        test_is_dominion()
        test_is_union()
        test_is_dynasty()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed!")
        sys.exit(1)
