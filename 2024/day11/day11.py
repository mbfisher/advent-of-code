import unittest
from pathlib import Path
from typing import Tuple, List


def next_stones(number: str) -> Tuple[str, ...]:
    if number == '0':
        return ('1',)

    if len(number) % 2 == 0:
        return str(int(number[:len(number) // 2])), str(int(number[len(number) // 2:]))

    return (str(int(number) * 2024),)


def blink(stones: List[str], repeat=1) -> List[str]:
    for i in range(repeat):
        result = []

        for number in stones:
            result.extend(next_stones(number))

        stones = result

    return result


def part1(input: str) -> int:
    return len(blink(input.split(" "), repeat=25))


def part2(input: str, repeat=75) -> int:
    stones = {number: 1 for number in input.split(" ")}

    for _ in range(repeat):
        blink = {}
        for number, freq in stones.items():
            for new in next_stones(number):
                blink[new] = blink.get(new, 0) + freq

        stones = blink

    return sum(stones.values())


class Test(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual("1 2024 1 0 9 9 2021976".split(" "), blink("0 1 10 99 999".split(" ")))
        self.assertEqual("2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2".split(" "),
                         blink("125 17".split(" "), repeat=6))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(55312, part2("125 17", repeat=25))

        print(part2(Path('./input.txt').read_text()))
