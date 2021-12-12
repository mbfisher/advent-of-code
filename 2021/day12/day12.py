from __future__ import annotations

from pathlib import Path
from typing import Set, Dict, List, Optional, Tuple


class Cave:
    def __init__(self, id: str):
        self.id = id
        self.big = id.isupper()
        self.connected_to: Set[Cave] = set()

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.id


def part1(input: str) -> List[List[Cave]]:
    caves: Dict[str, Cave] = {}

    start = caves.setdefault('start', Cave('start'))
    end = caves.setdefault('end', Cave('end'))

    for edge in input.splitlines():
        nodes = [caves.setdefault(id, Cave(id)) for id in edge.split("-")]
        nodes[0].connected_to.add(nodes[1])
        nodes[1].connected_to.add(nodes[0])

    paths: List[List[Cave]] = [[start]]

    while not all(path[-1] is end for path in paths):
        for path in filter(lambda path: path[-1] is not end, paths):
            for cave in path[-1].connected_to:
                if cave is start:
                    continue

                if cave.big or cave not in path:
                    new_path = list(path)
                    new_path.append(cave)
                    paths.append(new_path)

            paths.remove(path)

    return paths


def part2(input: str) -> Set[Tuple[Cave]]:
    caves: Dict[str, Cave] = {}

    start = caves.setdefault('start', Cave('start'))
    end = caves.setdefault('end', Cave('end'))

    for edge in input.splitlines():
        nodes = [caves.setdefault(id, Cave(id)) for id in edge.split("-")]
        nodes[0].connected_to.add(nodes[1])
        nodes[1].connected_to.add(nodes[0])

    paths: Set[Tuple[Cave]] = {(start,)}

    while not all(path[-1] is end for path in paths):
        incomplete_paths = set(filter(lambda path: path[-1] is not end, paths))
        for path in incomplete_paths:
            small_caves: Dict[str, int] = {}
            visited_twice: Optional[Cave] = None

            for small_cave in filter(lambda c: not c.big, path):
                small_caves.setdefault(small_cave.id, 0)
                small_caves[small_cave.id] += 1

                if small_caves[small_cave.id] == 2:
                    visited_twice = small_cave

                if small_caves[small_cave.id] > 2:
                    raise Exception(','.join([str(cave) for cave in path]))

            for cave in path[-1].connected_to:
                if cave is start:
                    continue

                if not cave.big and visited_twice and cave.id in small_caves:
                    continue

                paths.add(path + (cave,))

            paths.remove(path)

    return paths


if __name__ == '__main__':
    example1 = set(','.join([str(cave) for cave in path]) for path in part1('\n'.join([
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ])))

    assert example1 == {
        "start,A,b,A,c,A,end",
        "start,A,b,A,end",
        "start,A,b,end",
        "start,A,c,A,b,A,end",
        "start,A,c,A,b,end",
        "start,A,c,A,end",
        "start,A,end",
        "start,b,A,c,A,end",
        "start,b,A,end",
        "start,b,end",
    }, example1

    example2 = set(','.join([str(cave) for cave in path]) for path in part1('\n'.join([
        "dc-end",
        "HN-start",
        "start-kj",
        "dc-start",
        "dc-HN",
        "LN-dc",
        "HN-end",
        "kj-sa",
        "kj-HN",
        "kj-dc",
    ])))

    assert example2 == {
        "start,HN,dc,HN,end",
        "start,HN,dc,HN,kj,HN,end",
        "start,HN,dc,end",
        "start,HN,dc,kj,HN,end",
        "start,HN,end",
        "start,HN,kj,HN,dc,HN,end",
        "start,HN,kj,HN,dc,end",
        "start,HN,kj,HN,end",
        "start,HN,kj,dc,HN,end",
        "start,HN,kj,dc,end",
        "start,dc,HN,end",
        "start,dc,HN,kj,HN,end",
        "start,dc,end",
        "start,dc,kj,HN,end",
        "start,kj,HN,dc,HN,end",
        "start,kj,HN,dc,end",
        "start,kj,HN,end",
        "start,kj,dc,HN,end",
        "start,kj,dc,end"
    }, example2

    example3 = set(','.join([str(cave) for cave in path]) for path in part1('\n'.join([
        "fs-end",
        "he-DX",
        "fs-he",
        "start-DX",
        "pj-DX",
        "end-zg",
        "zg-sl",
        "zg-pj",
        "pj-he",
        "RW-he",
        "fs-DX",
        "pj-RW",
        "zg-RW",
        "start-pj",
        "he-WI",
        "zg-he",
        "pj-fs",
        "start-RW"
    ])))

    assert len(example3) == 226, len(example3)

    example4 = set(','.join([str(cave) for cave in path]) for path in part2('\n'.join([
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ])))

    assert example4 == {
        "start,A,b,A,b,A,c,A,end",
        "start,A,b,A,b,A,end",
        "start,A,b,A,b,end",
        "start,A,b,A,c,A,b,A,end",
        "start,A,b,A,c,A,b,end",
        "start,A,b,A,c,A,c,A,end",
        "start,A,b,A,c,A,end",
        "start,A,b,A,end",
        "start,A,b,d,b,A,c,A,end",
        "start,A,b,d,b,A,end",
        "start,A,b,d,b,end",
        "start,A,b,end",
        "start,A,c,A,b,A,b,A,end",
        "start,A,c,A,b,A,b,end",
        "start,A,c,A,b,A,c,A,end",
        "start,A,c,A,b,A,end",
        "start,A,c,A,b,d,b,A,end",
        "start,A,c,A,b,d,b,end",
        "start,A,c,A,b,end",
        "start,A,c,A,c,A,b,A,end",
        "start,A,c,A,c,A,b,end",
        "start,A,c,A,c,A,end",
        "start,A,c,A,end",
        "start,A,end",
        "start,b,A,b,A,c,A,end",
        "start,b,A,b,A,end",
        "start,b,A,b,end",
        "start,b,A,c,A,b,A,end",
        "start,b,A,c,A,b,end",
        "start,b,A,c,A,c,A,end",
        "start,b,A,c,A,end",
        "start,b,A,end",
        "start,b,d,b,A,c,A,end",
        "start,b,d,b,A,end",
        "start,b,d,b,end",
        "start,b,end"
    }, example4

    assert len(example4) == 36

    example5 = set(','.join([str(cave) for cave in path]) for path in part2('\n'.join([
        "dc-end",
        "HN-start",
        "start-kj",
        "dc-start",
        "dc-HN",
        "LN-dc",
        "HN-end",
        "kj-sa",
        "kj-HN",
        "kj-dc",
    ])))

    assert len(example5) == 103

    example6 = set(','.join([str(cave) for cave in path]) for path in part2('\n'.join([
        "fs-end",
        "he-DX",
        "fs-he",
        "start-DX",
        "pj-DX",
        "end-zg",
        "zg-sl",
        "zg-pj",
        "pj-he",
        "RW-he",
        "fs-DX",
        "pj-RW",
        "zg-RW",
        "start-pj",
        "he-WI",
        "zg-he",
        "pj-fs",
        "start-RW"
    ])))

    assert len(example6) == 3509

    input = Path('./input.txt').read_text()

    print(len(part1(input)))
    print(len(part2(input)))
