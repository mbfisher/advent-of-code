from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Set


class Octopi:
    def __init__(self, input: str):
        self.octopi: List[List[int]] = [list(map(int, line)) for line in input.splitlines()]
        self.flashes = 0

    def debug(self):
        return "\n".join("".join(map(str, row)) for row in self.octopi)

    def next(self):
        flash_queue: Set[Tuple[int, int]] = set()
        flashed: Set[Tuple[int, int]] = set()

        for i in range(0, len(self.octopi)):
            for j in range(0, len(self.octopi[i])):
                self.octopi[i][j] += 1

                if self.octopi[i][j] > 9:
                    self.flashes += 1
                    self.octopi[i][j] = 'x'
                    flash_queue.add((i, j))
                    flashed.add((i, j))

        while flash_queue:
            for i, j in list(flash_queue):
                for dy, dx in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
                    y = i + dy
                    x = j + dx

                    if y < 0 or x < 0:
                        continue

                    try:
                        if self.octopi[y][x] == 'x':
                            continue
                        self.octopi[y][x] += 1
                    except IndexError:
                        continue

                    if self.octopi[y][x] == 10:
                        self.flashes += 1
                        self.octopi[y][x] = 'x'
                        flash_queue.add((y, x))
                        flashed.add((y, x))

                flash_queue.remove((i, j))

        for i, j in flashed:
            self.octopi[i][j] = 0

        return self.debug()


def part1(input: str) -> int:
    octopi = Octopi(input)
    for _ in range(0, 100):
        octopi.next()

    return octopi.flashes


def part2(input: str) -> int:
    octopi = Octopi(input)
    step = 0
    while not all(all(o == 0 for o in row) for row in octopi.octopi):
        octopi.next()
        step += 1
    return step


if __name__ == '__main__':
    example = '\n'.join([
        "5483143223",
        "2745854711",
        "5264556173",
        "6141336146",
        "6357385478",
        "4167524645",
        "2176841721",
        "6882881134",
        "4846848554",
        "5283751526",
    ])

    input = Path('./input.txt').read_text()

    example1 = Octopi('\n'.join([
        "11111",
        "19991",
        "19191",
        "19991",
        "11111",
    ]))

    step1 = example1.next()
    assert step1 == '\n'.join([
        "34543",
        "40004",
        "50005",
        "40004",
        "34543",
    ]), step1

    step2 = example1.next()
    assert step2 == '\n'.join([
        "45654",
        "51115",
        "61116",
        "51115",
        "45654",
    ]), step2

    example2 = Octopi(example)

    step1 = example2.next()
    assert step1 == '\n'.join([
        "6594254334",
        "3856965822",
        "6375667284",
        "7252447257",
        "7468496589",
        "5278635756",
        "3287952832",
        "7993992245",
        "5957959665",
        "6394862637",
    ]), step1

    step2 = example2.next()
    assert step2 == '\n'.join([
        "8807476555",
        "5089087054",
        "8597889608",
        "8485769600",
        "8700908800",
        "6600088989",
        "6800005943",
        "0000007456",
        "9000000876",
        "8700006848",
    ]), step2

    example_part1 = part1(example)
    assert example_part1 == 1656, f"got {example_part1}"
    print(part1(input))

    example_part2 = part2(example)
    assert example_part2 == 195, f"got {example_part2}"
    print(part2(input))
