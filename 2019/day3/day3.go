package day3

import (
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"strings"
)

func createPath(operations []string) map[int]map[int]bool {
	path := map[int]map[int]bool{
		0: {
			0: true,
		},
	}

	var position = [2]int{0, 0}

	for _, op := range operations {
		runes := []rune(op)
		d := string(runes[0])
		m, _ := strconv.Atoi(string(runes[1:]))
		//fmt.Printf("d: %s, m: %d\n", d, m)

		for i := 1; i <= m; i++ {
			if d == "L" {
				position[0]--
			}
			if d == "R" {
				position[0]++
			}
			if d == "U" {
				position[1]++
			}
			if d == "D" {
				position[1]--
			}

			_, ok := path[position[0]]
			if !ok {
				path[position[0]] = map[int]bool{}
			}

			path[position[0]][position[1]] = true
		}
	}

	return path
}

func run(input string) {
	lines := strings.SplitN(input, "\n", 2)
	path1 := createPath(strings.Split(lines[0], ","))
	path2 := createPath(strings.Split(lines[1], ","))

	var points [][2]int

	for x, row := range path1 {
		for y, _ := range row {
			if path2[x][y] {
				point := [2]int{x, y}
				points = append(points, point)
			}
		}
	}

	fmt.Println(points)

	result := math.Abs(float64(points[0][0])) + math.Abs(float64(points[0][1]))
	var index int
	for i, point := range points {
		nextResult := math.Abs(float64(point[0])) + math.Abs(float64(point[1]))
		if nextResult > 0 && nextResult < result {
			result = nextResult
			index = i
		}
	}

	fmt.Println(points[index])
	fmt.Println(result)
}

func part1() {
	content, _ := ioutil.ReadFile("./day3/input.txt")
	run(string(content))
}

func Day3() {
	run("R8,U5,L5,D3\nU7,R6,D4,L4") // 3
	run("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83") // 159
	run("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7") // 135
	part1()
}
