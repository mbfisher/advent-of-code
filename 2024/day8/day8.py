import itertools
import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    city_map = input.splitlines()
    antennas = {}
    antinodes = set()

    for r, line in enumerate(city_map):
        for c, char in enumerate(line):
            if char == ".":
                continue

            antennas.setdefault(char, []).append((r, c))

    for frequency, locs in antennas.items():
        for a, b in itertools.combinations(locs, r=2):
            # pair[0] = (1, 8), pair[1] = (2, 5)
            # dy = 1, dx = -3
            dy, dx = b[0] - a[0], b[1] - a[1]

            # an1 = (3, 2)
            ana = (a[0] + dy * 2, a[1] + dx * 2)
            anb = (b[0] - dy * 2, b[1] - dx * 2)

            for an in (ana, anb):
                if 0 <= an[0] < len(city_map) and 0 <= an[1] < len(city_map[0]):
                    antinodes.add(an)

    # for locs in antennas.values():
    #     for loc in locs:
    #         antinodes.discard(loc)

    output = list(map(list, input.splitlines()))
    for r, c in antinodes:
        output[r][c] = '#'
    print('\n'.join(map(lambda line: ''.join(line), output)))

    return len(antinodes)


def part2(input: str, debug=False) -> int:
    return 0

class Test(unittest.TestCase):
    example1 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
    """.strip()

    def test_part_1(self):
        self.assertEqual(14, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(11387, part2(Test.example1, debug=True))

        print(part2(Path('./input.txt').read_text()))
