import unittest
from pathlib import Path


def part1(input: str) -> int:
    result = 0
    for line in input.split('\n'):
        ranges = (r.split('-') for r in line.split(','))
        elf1, elf2 = (set(range(int(start), int(end)+1)) for start, end in ranges)

        if len(elf1.difference(elf2)) == 0 or len(elf2.difference(elf1)) == 0:
            result += 1

    return result


def part2(input: str) -> int:
    result = 0
    for line in input.split('\n'):
        ranges = (r.split('-') for r in line.split(','))
        elf1, elf2 = (set(range(int(start), int(end)+1)) for start, end in ranges)

        if len(elf1.difference(elf2)) < len(elf1) or len(elf2.difference(elf1)) > len(elf2):
            result += 1

    return result


class Test(unittest.TestCase):
    example = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
    """.strip()

    def test_part_1(self):
        self.assertEqual(2, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(4, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))
