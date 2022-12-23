import unittest
from pathlib import Path


def mix(file: list[int], move: int = None):
    result = list(file)
    index = list(range(len(file)))

    moves = [file.index(move)] if move is not None else range(len(file))
    for i in moves:
        num = file[i]

        if num == 0:
            continue

        a = index.index(i)
        b = a + num

        if not 0 <= b < len(file):
            b %= len(file) - 1

        if num < 0 and b == 0:
            b = len(file) - 1
        if num > 0 and b == len(file) - 1:
            b = 0

        index.pop(a)
        index.insert(b, i)

        result = [file[i] for i in index]

    return result


def part1(input: str) -> int:
    file = list(map(int, input.split("\n")))

    decrypted = mix(file)

    zero = decrypted.index(0)
    return sum(decrypted[(i + zero) % len(file)] for i in [1000, 2000, 3000])


def part2(input: str) -> int:
    pass


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual([4, 5, 6, 7, 1, 8, 9], mix([4, 5, 6, 1, 7, 8, 9], move=1))
        self.assertEqual([4, 5, 6, 7, 8, -2, 9], mix([4, -2, 5, 6, 7, 8, 9], move=-2))
        self.assertEqual([1, 2, -3, 4, 0, 3, -2], mix([1, 2, -3, 3, -2, 0, 4]))
        self.assertEqual(3, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(58, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
1
2
-3
3
-2
0
4
""".strip("\n")
