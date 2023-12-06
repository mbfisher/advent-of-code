import unittest
from pathlib import Path

def part1(input: str) -> int:
    result = 0

    for line in input.split("\n"):
        winning, card = line.split(" | ")

        winning = winning.split(": ")[1]
        winning = set(map(int, filter(len, winning.split(" "))))

        card = set(map(int, filter(len, card.split(" "))))

        winners = winning.intersection(card)

        if len(winners) > 0:
            result += 2 ** (len(winners) - 1)

    return result


def part2(input: str) -> int:
    result = 0
    copies = {}

    for line in input.split("\n"):
        id = int(line.split(":")[0][5:])
        result += 1

        winning, card = line.split(" | ")

        winning = winning.split(": ")[1]
        winning = set(map(int, filter(len, winning.split(" "))))

        card = set(map(int, filter(len, card.split(" "))))

        matches = len(winning.intersection(card))

        if matches > 0:
            multiplyer = copies.get(id, 0) + 1
            for i in range(1, matches + 1):
                copy = id + i
                if copy not in copies:
                    copies[copy] = 0
                copies[copy] += multiplyer
                result += multiplyer

    return result



class Test(unittest.TestCase):
    example1 = '\n'.join([
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ])

    def test_part_1(self):
        self.assertEqual(13, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(30, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
