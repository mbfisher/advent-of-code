import logging
import multiprocessing
import time
import unittest
from multiprocessing import Pool, Manager, Value, Process
from pathlib import Path
from typing import Dict, List, Tuple, TypedDict


class Map:
    class Range(TypedDict):
        source: int
        dest: int
        len: int

    def __init__(self, name: str, ranges: List[Range]):
        self.name = name
        self.ranges = sorted(ranges, key=lambda r: r['dest'])
        self.example = list(map(lambda i: self.get(i), range(100)))

    def get(self, value):
        for rang in self.ranges:
            dest_range_start, source_range_start, range_len = rang['dest'], rang['source'], rang['len']

            if value < source_range_start:
                continue

            if value >= source_range_start + range_len:
                continue

            return dest_range_start + value - source_range_start

        return value

    def __str__(self):
        return f"<Map {self.name}>"


def parse(input: str) -> (List[int], Dict[str, Map]):
    lines = list(input.split("\n"))

    seeds_line = lines.pop(0)
    seeds = list(map(int, seeds_line[7:].split(" ")))
    lines.pop(0)

    maps: List[Map] = []
    map_name: str = ""
    map_ranges: List[Map.Range] = []
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
        map_ranges.append(Map.Range(source=source_range_start, dest=dest_range_start, len=range_len))

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


Range = Tuple[int, int, int]


def get_location(seed_range_start, seed_range_len, maps: List[List[Range]], progress: Value):
    result = float('Inf')
    count = 0
    for seed in range(seed_range_start, seed_range_start + seed_range_len):
        value = seed
        for map in maps:
            for rang in map:
                dest_range_start, source_range_start, range_len = rang

                if value < source_range_start:
                    continue

                if value >= source_range_start + range_len:
                    continue

                value = dest_range_start + value - source_range_start
                break

        if value < result:
            result = value

        count += 1
        if count % 1000 == 0:
            progress.value = progress.value + 1

    return result

def log_progress(progress: Value, total: int):
    while True:
        print("progress", progress.value, total, round(progress.value / total * 100, 1))
        time.sleep(1)


def part2(input: str) -> int:
    lines = list(input.split("\n"))

    seeds_line = lines.pop(0)
    seed_ranges = list(map(int, seeds_line[7:].split(" ")))
    seed_ranges = list((seed_ranges[i], seed_ranges[i + 1]) for i in range(0, len(seed_ranges), 2))
    lines.pop(0)

    total_seeds_before_optimisation = sum(r[1] for r in seed_ranges)
    print(total_seeds_before_optimisation, "seeds in", len(seed_ranges), "ranges before optimisation")
    optimised_ranges = optimise_seed_ranges(seed_ranges)
    total_seeds = sum(r[1] for r in optimised_ranges)
    print(total_seeds, "seeds in", len(optimised_ranges), "ranges after optimisation")
    print("optimisation removed", round((total_seeds_before_optimisation - total_seeds) / total_seeds, 0), "% of seeds")

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)

    with Manager() as manager:
        maps: List[List[Range]] = []

        map_ranges: List[Range] = []
        for line in lines:
            if line == "":
                maps.append(map_ranges)
                map_ranges = []
                continue

            if "map" in line:
                continue

            dest_range_start, source_range_start, range_len = tuple(map(int, filter(len, line.split(" "))))
            map_ranges.append((dest_range_start, source_range_start, range_len))

        maps.append(map_ranges)

        progress = manager.Value('i', 0)
        p = Process(target=log_progress, args=(progress, total_seeds))
        p.start()

        with Pool(max(len(optimised_ranges), 8)) as pool:
            locations = pool.starmap(get_location, [(seed_range_start, seed_range_len, maps, progress) for
                                        (seed_range_start, seed_range_len) in optimised_ranges])

        p.terminate()
        p.join()

        print("progress", progress.value)

        return min(locations)


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

        # self.assertEqual(46, part2(Path('./example1.txt').read_text()))

        # print(part2(Path('./input.txt').read_text()))
