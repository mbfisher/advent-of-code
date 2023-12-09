import unittest
from inspect import cleandoc
from pathlib import Path


def part1(input: str) -> int:
    return 0


def part2(input: str) -> int:
    return 0


class Test(unittest.TestCase):
    example1 = cleandoc("""
        """)

    def test_part_1(self):
        self.assertEqual(0, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(0, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
