import itertools
import unittest
from collections import deque
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from typing import Tuple, List, Set

moves = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
)


def regions(garden: Tuple[Tuple[str, ...], ...]) -> List[Set[Tuple[int, int]]]:
    unvisited = set((y, x) for x in range(len(garden[0])) for y in range(len(garden)))
    r = []

    while len(unvisited) > 0:
        py, px = unvisited.pop()
        plant = garden[py][px]

        queue = deque(((py, px),))
        region = set()

        while len(queue) > 0:
            y, x = queue.popleft()

            region.add((y, x))

            for dy, dx in moves:
                y1, x1 = (y + dy, x + dx)
                if (y1, x1) in unvisited and garden[y1][x1] == plant:
                    unvisited.remove((y1, x1))
                    queue.append((y1, x1))

        r.append(region)

    return r


def part1(input: str) -> int:
    garden = tuple(tuple(line) for line in input.splitlines())
    r = regions(garden)
    result = 0

    for region in r:
        area = len(region)
        perimeter = 0

        for y, x in region:
            for dy, dx in moves:
                y1, x1 = (y + dy, x + dx)
                if (y1, x1) not in region:
                    perimeter += 1

        result += area * perimeter

    return result


turns = {
    # top
    # A<.>A
    #  >A<
    (-1, 0): ((0, 0, 0, -1), (0, 0, 0, 1), (-1, -1, 0, 1), (-1, 1, 0, -1)),
    # right
    #   A
    #  v^
    #  A.
    #  ^v
    #   A
    (0, 1): ((0, 0, -1, 0), (0, 0, 1, 0), (-1, 1, 1, 0), (1, 1, -1, 0)),
    # bottom
    #  >A<
    # A<.>A
    (1, 0): ((0, 0, 0, 1), (0, 0, 0, -1), (1, -1, 0, 1), (1, 1, 0, -1)),
    # left
    #  A
    #  ^v
    #  .A
    #  v^
    #  A
    (0, -1): ((0, 0, 1, 0), (0, 0, -1, 0), (-1, -1, 1, 0), (1, -1, -1, 0))
}

def part2(input: str, repeat=75) -> int:
    garden = tuple(tuple(line) for line in input.splitlines())
    r = regions(garden)
    result = 0

    for region in r:
        area = len(region)
        perimeter = set()

        for y, x in region:
            for dy, dx in moves:
                y1, x1 = (y + dy, x + dx)
                if (y1, x1) not in region:
                    perimeter.add((y, x, dy, dx))

        sides = 0
        y = x = fy = fx = None

        while len(perimeter) > 0:
            if y is None:
                y, x, fy, fx = sorted(perimeter)[0]
                sides += 1

            try:
                perimeter.remove((y, x, fy, fx))
            except KeyError:
                raise

            corner = True
            for dy, dx in moves:
                y1, x1 = (y + dy, x + dx)
                if (y1, x1, fy, fx) in perimeter:
                    y, x = y1, x1
                    corner = False
                    break

            if corner:
                try:
                    y, x, fy, fx = next(((y + dy, x + dx, fy1, fx1) for dy, dx, fy1, fx1 in turns[(fy, fx)] if (y + dy, x + dx, fy1, fx1) in perimeter))
                    sides += 1
                except StopIteration:
                    y = None

        result += area * sides

    return result


class Test(unittest.TestCase):
    example1 = """
AAAA
BBCD
BBCC
EEEC
    """.strip()

    example2 = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
    """.strip()

    example3 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
    """.strip()

    example4 = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
    """.strip()

    example5 = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
    """.strip()

    def test_part_1(self):
        self.assertEqual(140, part1(self.example1))
        self.assertEqual(772, part1(self.example2))
        self.assertEqual(1930, part1(self.example3))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(80, part2(self.example1))
        self.assertEqual(236, part2(self.example4))
        self.assertEqual(368, part2(self.example5))
        self.assertEqual(1206, part2(self.example3))
        print(part2(Path('./input.txt').read_text()))
