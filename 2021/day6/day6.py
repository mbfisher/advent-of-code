import re
from dataclasses import dataclass
from math import ceil, floor
from pathlib import Path
from typing import List, TypedDict, Dict, Set, Tuple, Optional


def part1(input: str) -> int:
    fish: List[int] = list(map(int, input.split(",")))

    for day in range(0, 80):
        num_fish = len(fish)
        for i in range(0, num_fish):
            if fish[i] == 0:
                fish[i] = 6
                fish.append(8)
            else:
                fish[i] -= 1

    return len(fish)


def part2(input: str, num_days: int) -> int:
    fish: List[int] = list(map(int, input.split(",")))
    timers = {i: 0 for i in range(0, 9)}

    for timer in fish:
        timers[timer] += 1

    for day in range(0, num_days):
        new_fish = timers[0]

        for i in range(0, 8):
            timers[i] = timers[i + 1]

        timers[6] += new_fish
        timers[8] = new_fish

    return sum(count for _, count in timers.items())


if __name__ == '__main__':
    example = '\n'.join([
        "3,4,3,1,2"
    ])

    input = Path('./input.txt').read_text()

    example_part1 = part1(example)
    assert example_part1 == 5934, f"got {example_part1}"
    print(part1(input))

    example_part2a = part2(example, 18)
    assert example_part2a == 26, f"got {example_part2a}"
    example_part2b = part2(example, 80)
    assert example_part2b == 5934, f"got {example_part2b}"
    example_part2c = part2(example, 256)
    assert example_part2c == 26984457539, f"got {example_part2c}"

    print(part2(input, 256))
