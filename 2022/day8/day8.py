import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    grid = [list(map(int, row)) for row in input.split("\n")]

    visible_trees = set()

    for i, row in enumerate(grid):
        if i == 0 or i == len(grid)-1:
            for j, tree in enumerate(row):
                visible_trees.add((i, j))
            continue

        for j, tree in enumerate(row):
            if j == 0 or j == len(row)-1:
                visible_trees.add((i, j))
                continue

            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                visible = True
                next_tree = (i + direction[0], j + direction[1])

                while 0 <= next_tree[0] < len(grid) and 0 <= next_tree[1] < len(grid[0]):
                    if tree <= grid[next_tree[0]][next_tree[1]]:
                        visible = False
                        break

                    next_tree = (next_tree[0] + direction[0], next_tree[1] + direction[1])

                if visible:
                    visible_trees.add((i, j))

    return len(visible_trees)


def part2(input: str) -> int:
    grid = [list(map(int, row)) for row in input.split("\n")]

    visible_trees = set()
    result = 0

    for i, row in enumerate(grid):
        if i == 0 or i == len(grid)-1:
            for j, tree in enumerate(row):
                visible_trees.add((i, j))
            continue

        for j, tree in enumerate(row):
            if j == 0 or j == len(row)-1:
                visible_trees.add((i, j))
                continue

            scenic_score = 1

            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_tree = (i + direction[0], j + direction[1])

                while 0 <= next_tree[0] < len(grid) and 0 <= next_tree[1] < len(grid[0]):
                    if tree <= grid[next_tree[0]][next_tree[1]]:
                        break

                    if not(0 <= next_tree[0] + direction[0] < len(grid) and 0 <= next_tree[1] + direction[1] < len(grid[0])):
                        break

                    next_tree = (next_tree[0] + direction[0], next_tree[1] + direction[1])

                scenic_score *= abs(next_tree[0] - i + next_tree[1] - j)

            if scenic_score > result:
                result = scenic_score

    return result


class Test(unittest.TestCase):
    example = """
30373
25512
65332
33549
35390
""".strip("\n")

    def test_part_1(self):
        self.assertEqual(21, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(8, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))
