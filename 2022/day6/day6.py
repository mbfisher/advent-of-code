import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    for i in range(4, len(input)):
        if len(set(input[i-4:i])) == 4:
            return i


def part2(input: str) -> int:
    for i in range(14, len(input)):
        if len(set(input[i-14:i])) == 14:
            return i


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(7, part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb"))
        self.assertEqual(5, part1("bvwbjplbgvbhsrlpgdmjqwftvncz"))
        self.assertEqual(6, part1("nppdvjthqldpwncqszvftbrmjlhg"))
        self.assertEqual(10, part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"))
        self.assertEqual(11, part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(19, part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb"))
        self.assertEqual(23, part2("bvwbjplbgvbhsrlpgdmjqwftvncz"))
        self.assertEqual(23, part2("nppdvjthqldpwncqszvftbrmjlhg"))
        self.assertEqual(29, part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"))
        self.assertEqual(26, part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"))

        print(part2(Path('./input.txt').read_text()))
