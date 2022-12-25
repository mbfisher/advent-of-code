import unittest
from pathlib import Path


def mix(file: list[int], mixes=0):
    result = list(file)
    index = list(range(len(file)))

    for _ in range(mixes):
        for i in range(len(file)):
            num = file[i]

            if num == 0:
                continue

            a = index.index(i)
            b = a + num

            if not 0 <= b < len(file):
                b %= len(file) - 1

            if b == 0:
                b = len(file) - 1
            elif b == len(file) - 1:
                b = 0

            index.pop(a)
            index.insert(b, i)

            result = [file[i] for i in index]

    return result


def part1(input: str) -> int:
    file = list(map(int, input.split("\n")))

    decrypted = mix(file, mixes=1)

    zero = decrypted.index(0)
    return sum(decrypted[(i + zero) % len(file)] for i in [1000, 2000, 3000])


def part2(input: str) -> int:
    file = list(map(int, input.split("\n")))

    decrypted = mix([num * 811589153 for num in file], mixes=10)

    zero = decrypted.index(0)
    return sum(decrypted[(i + zero) % len(file)] for i in [1000, 2000, 3000])


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual([1, 2, -3, 4, 0, 3, -2], mix([1, 2, -3, 3, -2, 0, 4], mixes=1))
        self.assertEqual(3, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        # for i, result in enumerate([
        #     [0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153],
        #     [0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153],
        #     [0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459],
        #     [0, 1623178306, -2434767459, 811589153, 2434767459, 3246356612, -1623178306],
        #     [0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459],
        #     [0, 811589153, -1623178306, 3246356612, -2434767459, 1623178306, 2434767459],
        #     [0, -2434767459, 2434767459, 1623178306, -1623178306, 811589153, 3246356612],
        #     [0, 1623178306, 3246356612, 811589153, -2434767459, 2434767459, -1623178306],
        #     [0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306],
        #     [0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153],
        # ]):
        #     self.assertEqual(result,
        #                      mix([811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612],
        #                          mixes=i + 1),
        #                      msg=f"mixes={i + 1}")

        self.assertEqual(1623178306, part2(Test.example))

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
