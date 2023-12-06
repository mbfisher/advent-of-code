import time
import unittest
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

Range = Tuple[int, int, int]


class Map:
    def __init__(self, name: str, ranges: List[Range]):
        self.name = name
        self.ranges = sorted(ranges, key=lambda r: r[1])
        self.example = list(map(lambda i: self.get(i), range(100)))

    def get(self, value):
        for rang in self.ranges:
            dest_range_start, source_range_start, range_len = rang

            if value < source_range_start:
                continue

            if value >= source_range_start + range_len:
                continue

            return dest_range_start + value - source_range_start

        return value

    def get_range(self, rang):
        queue = deque([rang])
        result = []

        while bool(queue):
            source_start, source_len = queue.popleft()
            source_end = source_start + source_len - 1

            if all(source_start > dest_start + range_len for (dest_start, _, range_len) in self.ranges):
                result.append((source_start, source_len))
                continue

            if all(source_end < dest_start for (dest_start, _, range_len) in self.ranges):
                result.append((source_start, source_len))
                continue

            for (map_dest_start, map_source_start, map_len) in self.ranges:
                map_source_end = map_source_start + map_len - 1
                map_dest_end = map_dest_start + map_len - 1

                # hangs over the left
                if source_start < map_source_start <= source_end <= map_source_end:
                    subrange = (
                        source_start,
                        map_source_start - source_start
                    )
                    result.append(subrange)
                    queue.append((subrange[0] + subrange[1], subrange[1]))
                    break

                # fully contained
                if source_start >= map_source_start and source_end <= map_source_end:
                    result.append((map_dest_start + source_start - map_source_start, source_len))
                    break

                # hangs over the right
                if map_source_start <= source_start <= map_source_end:
                    subrange = (
                        map_dest_start + source_start - map_source_start,
                        min(source_len, map_source_end - source_start)
                    )
                    result.append(subrange)
                    queue.append((map_source_end + 1, subrange[1]))
                    break

        return result

    def __str__(self):
        return f"<Map {self.name}>"


def parse(input: str) -> (List[int], Dict[str, Map]):
    lines = list(input.split("\n"))

    seeds_line = lines.pop(0)
    seeds = list(map(int, seeds_line[7:].split(" ")))
    lines.pop(0)

    maps: List[Map] = []
    map_name: str = ""
    map_ranges: List[Range] = []
    for line in lines:
        if line == "":
            maps.append(Map(map_name, map_ranges))
            map_name = ""
            map_ranges = []
            continue

        if "map" in line:
            map_name = line.split(" ").pop(0)
            continue

        dest_range_start, source_range_start, range_len = tuple(map(int, filter(len, line.split(" "))))
        map_ranges.append((dest_range_start, source_range_start, range_len))

    maps.append(Map(map_name, map_ranges))

    return seeds, maps


def part1(input: str) -> int:
    seeds, maps = parse(input)

    locations = []
    for seed in seeds:
        # print("seed", seed)
        value = seed
        for map in maps:
            value = map.get(value)
            # print(map.name, value)

        locations.append(value)

    return min(locations)


def optimise_seed_ranges(seed_ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    optimised_ranges = []

    for r1 in sorted(seed_ranges, key=lambda r: r[0]):
        if not any(r2 for r2 in seed_ranges if r1 != r2 and r1[0] >= r2[0] and r1[0] + r1[1] <= r2[0] + r2[1]):
            optimised_ranges.append(r1)

    changed = True
    while changed:
        changed = False

        for i in range(len(optimised_ranges) - 1):
            a, b = optimised_ranges[i], optimised_ranges[i + 1]

            if b[0] <= a[0] + a[1]:
                optimised_ranges.remove(a)
                optimised_ranges.remove(b)
                optimised_ranges.insert(i, (a[0], b[0] + b[1]))
                changed = True
                break

    return optimised_ranges


def part2(input: str) -> int:
    seeds, maps = parse(input)
    seed_ranges = list((seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2))

    result = float('inf')

    for seed_range in seed_ranges:
        queue = [seed_range]
        for map in maps:
            # print(map.name, queue)
            next_queue = []
            for rang in queue:
                for next_range in map.get_range(rang):
                    next_queue.append(next_range)

            queue = next_queue.copy()

        if not queue:
            continue

        min_location = min(r[0] for r in queue)
        if min_location < result:
            result = min_location

    return result


class Test(unittest.TestCase):
    def test_part_1(self):
        seed_to_soil = Map("seed-to-soil", [(50, 98, 2), (52, 50, 48)])
        self.assertEqual(
            [0, 1, 48, 49, 52, 53, 98, 99, 50, 51],
            list(map(lambda seed: seed_to_soil.get(seed), [0, 1, 48, 49, 50, 51, 96, 97, 98, 99]))
        )

        self.assertEqual(35, part1(Path('./example1.txt').read_text()))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(
            [(1, 14), (20, 3), (60, 126)],
            optimise_seed_ranges([(5, 5), (1, 7), (60, 20), (8, 6), (20, 3), (2, 3), (70, 56)])
        )

        self.assertEqual(46, part2(Path('./example1.txt').read_text()))

        print(part2(Path('./input.txt').read_text()))

if __name__ == '__main__':
    start = time.time()
    part2(Path('./input.txt').read_text())
    print((time.time() - start) * 1000)
