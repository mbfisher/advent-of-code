import unittest
from inspect import cleandoc
from itertools import combinations
from pathlib import Path
from typing import Tuple, Dict


def parse_galaxies(input: str, expansion_rate: int) -> Dict[int, Tuple[int, int]]:
    image = list(list(row) for row in input.split("\n"))

    galaxies = {}
    id = 1

    for i, row in enumerate(image):
        for j in [k for k, value in enumerate(row) if value == "#"]:
            galaxies[id] = (i, j)
            id += 1

    expansion = {}

    for i in range(len(image)):
        if all(value == '.' for value in image[i]):
            for id in [k for k, pos in galaxies.items() if pos[0] > i]:
                if id not in expansion:
                    expansion[id] = (0, 0)
                expansion[id] = (expansion[id][0] + expansion_rate - 1, expansion[id][1])

    for j in range(len(image[0])):
        if all(row[j] == '.' for row in image):
            for id in [k for k, pos in galaxies.items() if pos[1] > j]:
                if id not in expansion:
                    expansion[id] = (0, 0)
                expansion[id] = (expansion[id][0], expansion[id][1] + expansion_rate - 1)

    for id, move in expansion.items():
        galaxies[id] = (galaxies[id][0] + move[0], galaxies[id][1] + move[1])

    return galaxies


def sum_shortest_paths(input: str, expansion_rate: int) -> int:
    galaxies = parse_galaxies(input, expansion_rate)
    result = 0

    for pair in combinations(range(1, len(galaxies) + 1), 2):
        x1, y1 = galaxies[pair[0]]
        x2, y2 = galaxies[pair[1]]

        steps = abs(x1 - x2) + abs(y1 - y2)

        result += steps

    return result


def part1(input: str) -> int:
    return sum_shortest_paths(input, 2)


def part2(input: str) -> int:
    return sum_shortest_paths(input, 1_000_000)


class Test(unittest.TestCase):
    example1 = cleandoc("""
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
    """)

    def test_part_1(self):
        self.assertEqual({
            1: (0, 4),
            2: (1, 9),
            3: (2, 0),
            4: (5, 8),
            5: (6, 1),
            6: (7, 12),
            7: (10, 9),
            8: (11, 0),
            9: (11, 5)
        }, parse_galaxies(Test.example1, 2))

        self.assertEqual(374, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(1030, sum_shortest_paths(Test.example1, 10))
        self.assertEqual(8410, sum_shortest_paths(Test.example1, 100))

        print(part2(Path('./input.txt').read_text()))
