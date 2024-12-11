import re
import unittest
from pathlib import Path


def part1(input: str, debug=False) -> int:
    word_search = input.split("\n")
    directions = (
        (0, 1),   # E
        (1, 1),   # SE
        (1, 0),   # S
        (1, -1),  # SW
        (-1, 0),  # W
        (-1, -1), # NW
        (-1, 0),  # N
        (-1, 1),  # NE
    )
    xmas = set()


    for row, line in enumerate(word_search):
        for col, char in enumerate(line):
            for move in directions:
                foreword, forecoords = "", []
                backword, backcoords = "", []

                for m in range(4):
                    fr, fc = row + move[0] * m, col + move[1] * m
                    br, bc = row - move[0] * m, col - move[1] * m
                    if 0 <= fr < len(word_search) and 0 <= fc < len(line):
                        foreword += word_search[fr][fc]
                        forecoords.append((fr, fc))
                    if 0 <= br < len(word_search) and 0 <= bc < len(line):
                        backword += word_search[br][bc]
                        backcoords.append((br, bc))

                if foreword == "XMAS":
                    xmas.add(tuple(forecoords))
                if backword == "XMAS":
                    xmas.add(tuple(backcoords))

    if debug:
        output = list(map(lambda line: ["."] * len(line), input.split("\n")))
        for coords in xmas:
            for r, c in coords:
                output[r][c] = word_search[r][c]
        print("\n".join(map(lambda line: "".join(line), output)))

    return len(xmas)


def part2(input: str) -> int:
    return 0


class Test(unittest.TestCase):
    example1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
    """.strip()

    example2 = ""

    def test_part_1(self):
        self.assertEqual(18, part1(Test.example1, debug=True))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(0, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))
