import re
import unittest
from functools import cache
from inspect import cleandoc
from itertools import permutations
from pathlib import Path
from typing import Tuple, Iterator

def recurse(string: str, groups: Tuple[int, ...], stats) -> (int, int):
    stats['invocations'] += 1

    wildcard = string.find('?')

    if wildcard == -1:
        contiguous = tuple(map(len, filter(len, string.split('.'))))

        if contiguous == groups:
            return 1

        return 0

    return (
        recurse(string[:wildcard] + '.' + string[wildcard + 1:], groups, stats) +
        recurse(string[:wildcard] + '#' + string[wildcard + 1:], groups, stats)
    )


def count_arrangements_recursive(row: str) -> int:
    springs, groups = row.split(" ")
    groups = tuple(map(int, groups.split(",")))

    stats = {'invocations': 0}
    result = recurse(springs, groups, stats)
    # print(row, stats)

    return result


def findall(char, string) -> Iterator[int]:
    i = string.find(char)
    while i > -1:
        yield i
        i = string.find(char, i + 1)


def count_arrangements_permutations(row: str) -> int:
    conditions, groups = row.split(" ")
    groups = tuple(map(int, groups.split(",")))

    unknowns = tuple(findall('?', conditions))

    existing_springs = conditions.count('#')
    springs_to_place = sum(groups) - existing_springs

    result = 0

    init = ('#' * springs_to_place) + ('.' * (conditions.count('?') - springs_to_place))
    all_perms = list(permutations(init))
    perms = set(all_perms)
    print(row, len(perms), len(all_perms))

    for perm in perms:
        arrangement = conditions
        for i in range(len(unknowns)):
            arrangement = arrangement[:unknowns[i]] + perm[i] + arrangement[unknowns[i] + 1:]

        contiguous = tuple(map(len, filter(len, arrangement.split('.'))))

        if contiguous == groups:
            result += 1

    return result


def part1(input: str) -> int:
    return sum(map(count_arrangements_recursive, input.split("\n")))


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
        # self.assertEqual(1, count_arrangements_permutations("???.### 1,1,3"))
        # self.assertEqual(4, count_arrangements_permutations(".??..??...?##. 1,1,3"))
        # self.assertEqual(1, count_arrangements_permutations("?#?#?#?#?#?#?#? 1,3,1,6"))
        # self.assertEqual(1, count_arrangements_permutations("????.#...#... 4,1,1"))
        # self.assertEqual(4, count_arrangements_permutations("????.######..#####. 1,6,5"))
        # self.assertEqual(10, count_arrangements_permutations("?###???????? 3,2,1"))

        self.assertEqual(21, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(0, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
