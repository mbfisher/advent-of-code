import re
import unittest
from functools import cache
from inspect import cleandoc
from pathlib import Path
from typing import Tuple


@cache
def recurse(string: str, groups: Tuple[int, ...]) -> int:
    wildcard = string.find('?')

    if wildcard == -1:
        contiguous = tuple(map(len, filter(len, string.split('.'))))

        if contiguous == groups:
            return 1

        return 0

    return (
        recurse(string[:wildcard] + '.' + string[wildcard + 1:], groups) +
        recurse(string[:wildcard] + '#' + string[wildcard + 1:], groups)
    )


def arrangements(row: str) -> int:
    springs, groups = row.split(" ")
    groups = tuple(map(int, groups.split(",")))

    return recurse(springs, groups)


def part1(input: str) -> int:
    return sum(map(arrangements, input.split("\n")))


def part2(input: str) -> int:
    return 0


class Test(unittest.TestCase):
    example1 = cleandoc("""
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
    """)

    def test_part_1(self):
        self.assertEqual(1, arrangements("???.### 1,1,3"))
        self.assertEqual(4, arrangements(".??..??...?##. 1,1,3"))
        self.assertEqual(1, arrangements("?#?#?#?#?#?#?#? 1,3,1,6"))
        self.assertEqual(1, arrangements("????.#...#... 4,1,1"))
        self.assertEqual(4, arrangements("????.######..#####. 1,6,5"))
        self.assertEqual(10, arrangements("?###???????? 3,2,1"))

        self.assertEqual(21, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(0, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
