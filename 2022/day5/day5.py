import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> str:
    lines = input.split('\n')
    stacks = [deque() for _ in range((len(lines[0]) + 1) // 4)]
    fill_stacks = True

    for line in lines:
        if not line:
            continue

        if fill_stacks and "[" not in line:
            fill_stacks = False
            continue

        if fill_stacks:
            for i in range(len(stacks)):
                try:
                    crate = line[i * 4 + 1]
                except IndexError:
                    raise
                if crate != " ":
                    stacks[i].appendleft(crate)
        else:
            n, f, t = tuple(int(part) for part in line.split() if part.isnumeric())
            for _ in range(n):
                stacks[t - 1].append(stacks[f - 1].pop())

    return "".join([stack.pop() for stack in stacks])


def part2(input: str) -> str:
    lines = input.split('\n')
    stacks = [deque() for _ in range((len(lines[0]) + 1) // 4)]
    fill_stacks = True

    for line in lines:
        if not line:
            continue

        if fill_stacks and "[" not in line:
            fill_stacks = False
            continue

        if fill_stacks:
            for i in range(len(stacks)):
                try:
                    crate = line[i * 4 + 1]
                except IndexError:
                    raise
                if crate != " ":
                    stacks[i].appendleft(crate)
        else:
            n, f, t = tuple(int(part) for part in line.split() if part.isnumeric())
            move = deque()
            for _ in range(n):
                move.append(stacks[f - 1].pop())
            while move:
                stacks[t - 1].append(move.pop())

    return "".join([stack.pop() for stack in stacks])


class Test(unittest.TestCase):
    example = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".strip("\n")

    def test_part_1(self):
        self.assertEqual("CMZ", part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual("MCD", part2(Test.example))

        print(part2(Path('./input.txt').read_text()))
