import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    X = 1
    instructions = deque(input.split("\n"))
    addx = None
    result = 0

    for cycle in range(1, 221):
        if not addx:
            next_instruction = instructions.popleft()

            if next_instruction != "noop":
                value = int(next_instruction.split(" ")[1])
                addx = (cycle + 1, value)

        if (cycle + 20) % 40 == 0:
            signal_strength = cycle * X
            result += signal_strength

        if addx and addx[0] == cycle:
            X += addx[1]
            addx = None

    return result


def part2(input: str) -> str:
    X = 1
    instructions = deque(input.split("\n"))
    addx = None

    crt = ""

    for cycle in range(0, 240):
        if not addx:
            next_instruction = instructions.popleft()

            if next_instruction != "noop":
                value = int(next_instruction.split(" ")[1])
                addx = (cycle + 1, value)

        if cycle - (cycle // 40) * 40 in [X - 1, X, X + 1]:
            crt += "#"
        else:
            crt += "."

        if (cycle + 1) % 40 == 0:
            crt += "\n"

        if addx and addx[0] == cycle:
            X += addx[1]
            addx = None

    return crt


class Test(unittest.TestCase):

    def test_part_1(self):
        #         self.assertEqual(None, part1("""
        # noop
        # addx 3
        # addx -5""".strip("\n")))

        self.assertEqual(13140, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        result = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....""".strip("\n") + "\n"

        self.assertEqual(result, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip("\n")
