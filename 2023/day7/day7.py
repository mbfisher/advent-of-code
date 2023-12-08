import unittest
from functools import cmp_to_key
from pathlib import Path

CARDS1 = {card: score for score, card in enumerate(["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"])}
CARDS2 = {card: score for score, card in
          enumerate(["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"])}


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


def comparator1(a: str, b: str) -> int:
    score_a = type_score(a)
    score_b = type_score(b)

    if score_a != score_b:
        return score_a - score_b

    for i in range(5):
        if a[i] == b[i]:
            continue

        return CARDS1[a[i]] - CARDS1[b[i]]


def comparator2(a: str, b: str) -> int:
    score_a = type_score(apply_jokers(a))
    score_b = type_score(apply_jokers(b))

    if score_a != score_b:
        return score_a - score_b

    for i in range(5):
        if a[i] == b[i]:
            continue

        return CARDS2[a[i]] - CARDS2[b[i]]


def apply_jokers(hand: str) -> str:
    num_jokers = hand.count("J")
    if num_jokers == 0:
        return hand

    if num_jokers == 5:
        return "AAAAA"

    kind = set([card for card in hand if card != "J"])

    def sort_by_count_and_strength(a, b):
        count_a = hand.count(a)
        count_b = hand.count(b)

        if count_a != count_b:
            return count_a - count_b

        return CARDS1[a] - CARDS2[b]

    sorted_cards = sorted(kind, reverse=True, key=cmp_to_key(sort_by_count_and_strength))

    return hand.replace("J", sorted_cards[0])


def play(input: str, comparator) -> int:
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


def part1(input: str) -> int:
    return play(input, comparator1)


def part2(input: str) -> int:
    return play(input, comparator2)


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

        self.assertGreater(comparator1("33332", "2AAAA"), 0)
        self.assertLess(comparator1("77788", "77888"), 0)

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
        ], key=cmp_to_key(comparator1)))

        self.assertEqual(6440, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        # one joker
        # high card -> one pair
        self.assertEqual("23455", apply_jokers("2345J"))
        # two pair -> full house
        self.assertIn(apply_jokers("2233J"), "22333")
        # three of a kind -> four of a kind
        self.assertEqual("QQQQK", apply_jokers("QQQJK"))
        # four of a kind -> five of a kind
        self.assertEqual("QQQQQ", apply_jokers("QQQQJ"))

        # two jokers
        # high card -> three of a kind
        self.assertEqual("23444", apply_jokers("234JJ"))
        # one pair -> four of a kind
        self.assertEqual("23333", apply_jokers("233JJ"))
        # three of a kind -> five of a kind
        self.assertEqual("33333", apply_jokers("333JJ"))

        # three jokers
        # high card -> four of a kind
        self.assertEqual("23333", apply_jokers("23JJJ"))
        # one pair -> five of a kind
        self.assertEqual("22222", apply_jokers("22JJJ"))

        # four jokers
        # high card -> five of a kind
        self.assertEqual("22222", apply_jokers("2JJJJ"))

        # inputs
        # four of a kind better than full house
        self.assertEqual("TTTQT", apply_jokers("TTJQT"))
        self.assertEqual("33KA3", apply_jokers("33KAJ"))
        self.assertEqual("55666", apply_jokers("556J6"))
        self.assertEqual("Q6Q6Q", apply_jokers("Q6Q6J"))
        self.assertEqual("22272", apply_jokers("2J27J"))
        self.assertEqual("KQ4KK", apply_jokers("JQ4JK"))
        self.assertEqual("66666", apply_jokers("J6JJ6"))
        self.assertEqual("57Q6Q", apply_jokers("57J6Q"))
        self.assertEqual("4T744", apply_jokers("JT744"))
        self.assertEqual("49T8T", apply_jokers("49T8J"))

        self.assertLess(comparator2("JKKK2", "QQQQ2"), 0)

        self.assertEqual([
            "32T3K",
            "KK677",
            "T55J5",
            "QQQJA",
            "KTJJT",
        ], sorted([
            "T55J5",
            "QQQJA",
            "KK677",
            "32T3K",
            "KTJJT",
        ], key=cmp_to_key(comparator2)))

        self.assertEqual(5905, part2(Test.example1))

        input = Path('./input.txt').read_text()
        hands = [line.split(" ")[0] for line in input.split("\n")]
        joker_hands = [hand for hand in hands if "J" in hand]
        multi_joker_hands = [hand for hand in joker_hands if hand.count("J") >= 2]

        print(part2(Path('./input.txt').read_text()))
