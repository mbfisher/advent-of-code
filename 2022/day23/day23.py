import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    grove = {}
    for row, line in enumerate(input.split("\n")):
        for column, char in enumerate(line):
            if char == "#":
                grove.setdefault(row, {}).setdefault(column, True)

    north = (-1, 0)
    north_east = (-1, 1)
    east = (0, 1)
    south_east = (1, 1)
    south = (1, 0)
    south_west = (1, -1)
    west = (0, -1)
    north_west = (-1, -1)

    proposals = deque([
        (north, north_east, north_west),
        (south, south_east, south_west),
        (west, north_west, south_west),
        (east, north_east, south_east)
    ])

    for _ in range(10):
        moves = {}

        for row in grove.keys():
            for column in grove[row].keys():
                elf = (row, column)

                has_neighbours = False
                for direction in [north, north_east, east, south_east, south, south_west, west, north_west]:
                    if grove.get(row + direction[0], {}).get(column + direction[1], None) is not None:
                        has_neighbours = True
                        break

                if not has_neighbours:
                    continue

                for proposal in proposals:
                    if all(grove.get(row + direction[0], {}).get(column + direction[1], None) is None
                           for direction in proposal):
                        moves[(row, column)] = (row + proposal[0][0], column + proposal[0][1])
                        break

        if len(moves) == 0:
            break

        collisions = {}
        for elf, move in moves.items():
            collisions.setdefault(move, 0)
            collisions[move] += 1

        for elf, move in moves.items():
            if collisions[move] > 1:
                continue

            grove[elf[0]].pop(elf[1])
            if len(grove[elf[0]]) == 0:
                grove.pop(elf[0])
            grove.setdefault(move[0], {}).setdefault(move[1], True)

        proposals.append(proposals.popleft())

        # rows = grove.keys()
        # columns = tuple(column for row in grove.values() for column in row.keys())
        # output = ""
        # for row in range(min(rows) - 1, max(rows) + 2):
        #     for column in range(min(columns) - 1, max(columns) + 2):
        #         if grove.get(row, {}).get(column, None) is not None:
        #             output += "#"
        #         else:
        #             output += "."
        #     output += "\n"
        # print(output)

    rows = grove.keys()
    columns = tuple(column for row in grove.values() for column in row.keys())
    result = 0
    for row in range(min(rows), max(rows) + 1):
        for column in range(min(columns), max(columns) + 1):
            if grove.get(row, {}).get(column, None) is None:
                result += 1

    return result


def part2(input: str) -> int:
    grove = {}
    for row, line in enumerate(input.split("\n")):
        for column, char in enumerate(line):
            if char == "#":
                grove.setdefault(row, {}).setdefault(column, True)

    north = (-1, 0)
    north_east = (-1, 1)
    east = (0, 1)
    south_east = (1, 1)
    south = (1, 0)
    south_west = (1, -1)
    west = (0, -1)
    north_west = (-1, -1)

    proposals = deque([
        (north, north_east, north_west),
        (south, south_east, south_west),
        (west, north_west, south_west),
        (east, north_east, south_east)
    ])

    rounds = 0
    while True:
        rounds += 1
        moves = {}

        for row in grove.keys():
            for column in grove[row].keys():
                elf = (row, column)

                has_neighbours = False
                for direction in [north, north_east, east, south_east, south, south_west, west, north_west]:
                    if grove.get(row + direction[0], {}).get(column + direction[1], None) is not None:
                        has_neighbours = True
                        break

                if not has_neighbours:
                    continue

                for proposal in proposals:
                    if all(grove.get(row + direction[0], {}).get(column + direction[1], None) is None
                           for direction in proposal):
                        moves[(row, column)] = (row + proposal[0][0], column + proposal[0][1])
                        break

        if len(moves) == 0:
            break

        collisions = {}
        for elf, move in moves.items():
            collisions.setdefault(move, 0)
            collisions[move] += 1

        for elf, move in moves.items():
            if collisions[move] > 1:
                continue

            grove[elf[0]].pop(elf[1])
            if len(grove[elf[0]]) == 0:
                grove.pop(elf[0])
            grove.setdefault(move[0], {}).setdefault(move[1], True)

        proposals.append(proposals.popleft())

    return rounds

class Test(unittest.TestCase):

    def test_part_1(self):
        part1(Test.example1)
        self.assertEqual(110, part1(Test.example2))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(20, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))

    example1 = """
.....
..##.
..#..
.....
..##.
.....
""".strip("\n")

    example2 = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".strip("\n")