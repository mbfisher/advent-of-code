import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    root = {
        "type": "dir",
        "name": "/",
        "parent": None,
        "children": [],
        "size": 0
    }
    dirs = {
        ("/",): root
    }
    files = {}
    current_dir = None
    current_path = ()

    for line in input.split("\n"):
        if line[0] == "$":
            command = line.split(" ")
            if command[1] == "cd":
                next_path = list(current_path)
                if command[2] == "..":
                    next_path.pop()
                else:
                    next_path.append(command[2])

                current_path = tuple(next_path)
                current_dir = dirs[current_path]
        else:
            info = line.split(" ")

            if info[0] == "dir":
                new_dir = {
                    "type": "dir",
                    "name": info[1],
                    "parent": current_path,
                    "children": [],
                    "size": 0
                }
                current_dir["children"].append(new_dir)
                dirs[tuple(list(current_path) + [new_dir['name']])] = new_dir
            else:
                file = {
                    "type": "file",
                    "name": info[1],
                    "size": int(info[0]),
                    "parent": current_path
                }
                current_dir["children"].append(file)
                files[tuple(list(current_path) + [file['name']])] = file

                parent = file["parent"]
                while parent:
                    dirs[parent]["size"] += file["size"]
                    parent = dirs[parent]["parent"]

    return sum(dir["size"] for dir in dirs.values() if dir["size"] <= 100000)


def part2(input: str) -> int:
    root = {
        "type": "dir",
        "name": "/",
        "parent": None,
        "children": [],
        "size": 0
    }
    dirs = {
        ("/",): root
    }
    files = {}
    current_dir = None
    current_path = ()

    for line in input.split("\n"):
        if line[0] == "$":
            command = line.split(" ")
            if command[1] == "cd":
                next_path = list(current_path)
                if command[2] == "..":
                    next_path.pop()
                else:
                    next_path.append(command[2])

                current_path = tuple(next_path)
                current_dir = dirs[current_path]
        else:
            info = line.split(" ")

            if info[0] == "dir":
                new_dir = {
                    "type": "dir",
                    "name": info[1],
                    "parent": current_path,
                    "children": [],
                    "size": 0
                }
                current_dir["children"].append(new_dir)
                dirs[tuple(list(current_path) + [new_dir['name']])] = new_dir
            else:
                file = {
                    "type": "file",
                    "name": info[1],
                    "size": int(info[0]),
                    "parent": current_path
                }
                current_dir["children"].append(file)
                files[tuple(list(current_path) + [file['name']])] = file

                parent = file["parent"]
                while parent:
                    dirs[parent]["size"] += file["size"]
                    parent = dirs[parent]["parent"]

    target = 30000000
    used_space = dirs[("/",)]["size"]
    unused_space = 70000000 - used_space
    result = float("inf")
    for dir in dirs.values():
        if unused_space + dir["size"] >= target and dir["size"] < result:
            result = dir["size"]

    return result


class Test(unittest.TestCase):
    example = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip("\n")

    def test_part_1(self):
        self.assertEqual(95437, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(24933642, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))
