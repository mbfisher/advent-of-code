from pathlib import Path
from typing import List


def part1(input: str) -> int:
    measurements = [int(line) for line in input.split('\n')]

    result = 0
    for i in range(1, len(measurements)):
        if measurements[i] > measurements[i - 1]:
            result += 1

    return result


def part2(input: str) -> int:
    measurements = [int(line) for line in input.split('\n')]

    windows = []
    for i in range(2, len(measurements)):
        windows.append(measurements[i] + measurements[i-1] + measurements[i-2])

    result = 0
    for i in range(1, len(windows)):
        if windows[i] > windows[i - 1]:
            result += 1

    return result


if __name__ == '__main__':
    example = '\n'.join([
        "199",
        "200",
        "208",
        "210",
        "200",
        "207",
        "240",
        "269",
        "260",
        "263",
    ])

    assert part1(example) == 7
    print(part1(Path('./input.txt').read_text()))

    assert part2(example) == 5
    print(part2(Path('./input.txt').read_text()))
