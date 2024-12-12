import unittest
from functools import cmp_to_key
from pathlib import Path
from typing import Tuple, List, Dict, Set


turn_right = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}

pointers = {
    (-1, 0): '^',
    (0, 1): '>',
    (1, 0): 'v',
    (0, -1): '<',
}

def part1(input: str, debug=False) -> int:
    lab = list(map(list, input.splitlines()))
    pos = next((i, row.index('^')) for i, row in enumerate(lab) if '^' in row)
    move = (-1, 0)
    positions = {pos}

    while 0 <= pos[0] + move[0] < len(lab) and 0 <= pos[1] + move[1] < len(lab[0]):
        if debug:
            print("\n".join(
                "".join(pointers[move] if (i, j) == pos else char for j, char in enumerate(line))
                for i, line in enumerate(lab)
            ) + "\n")

        if lab[pos[0] + move[0]][pos[1] + move[1]] == '#':
            move = turn_right[move]
        else:
            pos = (pos[0] + move[0], pos[1] + move[1])
            positions.add(pos)

    return len(positions)


def part2(input: str) -> int:
    return 0


class Test(unittest.TestCase):
    example1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
    """.strip()

    def test_part_1(self):
        self.assertEqual(41, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(123, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
