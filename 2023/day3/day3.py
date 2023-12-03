import unittest
from pathlib import Path

NUMBERS = set("1234567890")
DIRECTIONS = (
    (-1, 0),  # N
    (-1, 1),  # NE
    (0, 1),  # E
    (1, 1),  # SE
    (1, 0),  # S
    (1, -1),  # SW
    (0, -1),  # W
    (-1, -1),  # NW
)


def part1(input: str) -> int:
    # for each location
    # check adjacent
    # if number
    #   check visited number set
    #   walk forward and back along row
    # store visited number locations in a set

    schematic = input.split("\n")
    result = 0
    visited = set()

    for r in range(len(schematic)):
        row = schematic[r]
        for c in range(len(row)):
            if schematic[r][c] == "." or schematic[r][c] in NUMBERS:
                continue

            for move in DIRECTIONS:
                dr, dc = r + move[0], c + move[1]

                if dr < 0 or dr > len(schematic) - 1 or dc < 0 or dc > len(row) - 1:
                    continue

                if (dr, dc) in visited:
                    continue

                if schematic[dr][dc] in NUMBERS:
                    nrow = schematic[dr]
                    nr, nc = dr, dc
                    number = nrow[nc]

                    while nc >= 0:
                        nc -= 1
                        if nrow[nc] in NUMBERS:
                            number = nrow[nc] + number
                            visited.add((nr, nc))
                        else:
                            break

                    nc = dc
                    while nc < len(nrow) - 1:
                        nc += 1
                        if nrow[nc] in NUMBERS:
                            number = number + nrow[nc]
                            visited.add((nr, nc))
                        else:
                            break

                    result += int(number)

    return result


def part2(input: str) -> int:
    schematic = input.split("\n")
    result = 0
    visited = set()

    for r in range(len(schematic)):
        row = schematic[r]
        for c in range(len(row)):
            if schematic[r][c] != "*":
                continue

            gear_ratio = 1
            part_numbers = 0

            for move in DIRECTIONS:
                dr, dc = r + move[0], c + move[1]

                if dr < 0 or dr > len(schematic) - 1 or dc < 0 or dc > len(row) - 1:
                    continue

                if (dr, dc) in visited:
                    continue

                if schematic[dr][dc] in NUMBERS:
                    nrow = schematic[dr]
                    nr, nc = dr, dc
                    number = nrow[nc]

                    while nc >= 0:
                        nc -= 1
                        if nrow[nc] in NUMBERS:
                            number = nrow[nc] + number
                            visited.add((nr, nc))
                        else:
                            break

                    nc = dc
                    while nc < len(nrow) - 1:
                        nc += 1
                        if nrow[nc] in NUMBERS:
                            number = number + nrow[nc]
                            visited.add((nr, nc))
                        else:
                            break

                    gear_ratio *= int(number)
                    part_numbers += 1

            if part_numbers == 2:
                result += gear_ratio

    return result


class Test(unittest.TestCase):
    example1 = '\n'.join([
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ])

    def test_part_1(self):
        self.assertEqual(4361, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(467835, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
