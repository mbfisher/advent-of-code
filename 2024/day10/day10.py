import unittest
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

moves = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
)


def parse(input: str) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(-1 if pos == '.' else int(pos) for pos in line) for line in input.splitlines())


def score(trailhead: Tuple[int, int], topmap: Tuple[Tuple[int, ...], ...]) -> int:
    nines = set()
    stack = deque([(trailhead,)])

    while len(stack) > 0:
        trail = stack.pop()

        r, c = trail[-1]

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(topmap) and 0 <= nc < len(topmap[0]) and topmap[nr][nc] == topmap[r][c] + 1:
                if topmap[nr][nc] == 9:
                    nines.add((nr, nc))
                else:
                    stack.append(trail + ((nr, nc),))

    return len(nines)


def part1(input: str) -> int:
    topmap = parse(input)
    result = 0

    for i, row in enumerate(topmap):
        for j, pos in enumerate(row):
            if pos == 0:
                result += score((i, j), topmap)

    return result


def rating(trailhead: Tuple[int, int], topmap: Tuple[Tuple[int, ...], ...]) -> int:
    result = 0
    stack = deque([(trailhead,)])

    while len(stack) > 0:
        trail = stack.pop()

        r, c = trail[-1]

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(topmap) and 0 <= nc < len(topmap[0]) and topmap[nr][nc] == topmap[r][c] + 1:
                if topmap[nr][nc] == 9:
                    result += 1
                else:
                    stack.append(trail + ((nr, nc),))

    return result


def part2(input: str) -> int:
    topmap = parse(input)
    result = 0

    for i, row in enumerate(topmap):
        for j, pos in enumerate(row):
            if pos == 0:
                result += rating((i, j), topmap)

    return result


class Test(unittest.TestCase):
    example1 = """
0123
1234
8765
9876
    """.strip()

    example2 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
    """.strip()

    def test_part_1(self):
        self.assertEqual(1, score((0, 0), parse("""
0123
1234
8765
9876
        """.strip())))

        self.assertEqual(2, score((0, 3), parse("""
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
        """.strip())))

        self.assertEqual(4, score((0, 3), parse("""
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
        """.strip())))

        self.assertEqual(36, part1(Test.example2))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(3, rating((0, 5), parse("""
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
        """.strip())))

        self.assertEqual(13, rating((0, 3), parse("""
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
        """.strip())))

        self.assertEqual(227, rating((0, 0), parse("""
012345
123456
234567
345678
4.6789
56789.
        """.strip())))

        self.assertEqual(81, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))
