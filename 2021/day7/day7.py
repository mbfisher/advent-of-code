from pathlib import Path
from typing import List


def part1(input: str) -> int:
    crabs: List[int] = list(map(int, input.split(',')))

    results: List[int] = []
    for align in range(min(crabs), max(crabs)+1):
        results.append(sum(abs(position - align) for position in crabs))

    return min(results)


def part2(input: str) -> int:
    # 1 = 1
    # 2 = 1 + 2 = 3
    # 3 = 1 + 2 + 3 = 6
    crabs: List[int] = list(map(int, input.split(',')))

    def fuel_burn(position: int, align: int):
        n = abs(position - align)
        return int(n * (n + 1) / 2)

    results: List[int] = []
    for align in range(min(crabs), max(crabs) + 1):
        results.append(sum(fuel_burn(position, align) for position in crabs))

    return min(results)


if __name__ == '__main__':
    example = '\n'.join([
        "16,1,2,0,4,2,7,1,2,14"
    ])

    input = Path('./input.txt').read_text()

    example_part1 = part1(example)
    assert example_part1 == 37, f"got {example_part1}"
    print(part1(input))

    example_part2 = part2(example)
    assert example_part2 == 168, f"got {example_part2}"
    print(part2(input))
