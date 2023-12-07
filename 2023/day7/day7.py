import unittest
from functools import cmp_to_key
from pathlib import Path

CARDS = {card: score for score, card in enumerate(["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"])}


def type_score(hand: str) -> int:
    kind = set(hand)

    # High card
    if len(kind) == 5:
        return 1

    # Five of a kind
    if len(kind) == 1:
        return 7

    if len(kind) == 2:
        # Four of a kind
        if any(hand.count(card) == 4 for card in kind):
            return 6

        # Full house
        return 5

    if len(kind) == 3:
        # Three of a kind
        if any(hand.count(card) == 3 for card in kind):
            return 4

        # Two pair
        return 3

    # One pair
    return 2


def comparator(a: str, b: str) -> int:
    score_a = type_score(a)
    score_b = type_score(b)

    if score_a != score_b:
        return score_a - score_b

    for i in range(5):
        if a[i] == b[i]:
            continue

        return CARDS[a[i]] - CARDS[b[i]]


def part1(input: str) -> int:
    hands = []
    bids = {}

    for line in input.split("\n"):
        hand, bid = list(filter(len, line.split(" ")))
        hands.append(hand)
        bids[hand] = int(bid)

    hands.sort(key=cmp_to_key(comparator))

    result = 0
    for i in range(1, len(hands) + 1):
        result += bids[hands[i - 1]] * i

    return result


def part2(input: str) -> int:
    return 0


class Test(unittest.TestCase):
    example1 = '\n'.join([
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ])

    def test_part_1(self):
        self.assertEqual(7, type_score("AAAAA"))
        self.assertEqual(6, type_score("AA8AA"))
        self.assertEqual(5, type_score("23332"))
        self.assertEqual(4, type_score("TTT98"))
        self.assertEqual(3, type_score("23432"))
        self.assertEqual(2, type_score("A23A4"))
        self.assertEqual(1, type_score("23456"))

        self.assertGreater(comparator("33332", "2AAAA"), 0)
        self.assertLess(comparator("77788", "77888"), 0)

        self.assertEqual([
            "32T3K",
            "KTJJT",
            "KK677",
            "T55J5",
            "QQQJA"
        ], sorted([
            "T55J5",
            "QQQJA",
            "KK677",
            "32T3K",
            "KTJJT",
        ], key=cmp_to_key(comparator)))

        self.assertEqual(6440, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(0, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
