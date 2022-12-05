import unittest
from pathlib import Path


def part1(input: str) -> int:
    current = 0
    result = 0

    for line in input.split("\n"):
        if line == "":
            if current > result:
                result = current
            current = 0
        else:
            current += int(line)

    return result




def part2(input: str) -> int:
    current = 0
    top3 = []

    for line in input.split("\n"):
        if line == "":
            top3.append(current)
            if len(top3) > 3:
                top3.sort(reverse=True)
                top3.pop()

            current = 0
        else:
            current += int(line)

    top3.append(current)
    if len(top3) > 3:
        top3.sort(reverse=True)
        top3.pop()

    return sum(top3)


class Test(unittest.TestCase):
    example1 = '\n'.join([
        "1000",
        "2000",
        "3000",
        "",
        "4000",
        "",
        "5000",
        "6000",
        "",
        "7000",
        "8000",
        "9000",
        "",
        "10000",
    ])

    def test_part_1(self):
        self.assertEqual(24000, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(45000, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))