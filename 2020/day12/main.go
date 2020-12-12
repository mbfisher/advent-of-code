package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
)

func getManhattanDistance(scanner *bufio.Scanner) int {
	position := make([]int, 2)
	movements := map[string][]int{
		"N": {1, 0},
		"E": {0, 1},
		"S": {-1, 0},
		"W": {0, -1},
	}
	heading := 90
	compass := map[int]string {
		0: "N",
		90: "E",
		180: "S",
		270: "W",
	}

	move := func(direction string, value int) {
		position[0] = position[0] + movements[direction][0] * value
		position[1] = position[1] + movements[direction][1] * value
	}

	for scanner.Scan() {
		instruction := scanner.Text()
		action := string(instruction[0])
		value, _ := strconv.Atoi(instruction[1:])

		switch action {
		case "N", "S", "E", "W":
			move(action, value)
			break
		case "F":
			move(compass[heading], value)
			break
		case "R":
			heading += value
			if heading >= 360 {
				heading -= 360
			}
			break
		case "L":
			heading -= value
			if heading < 0 {
				heading += 360
			}
			break
		}
	}

	return int(math.Abs(float64(position[0])) + math.Abs(float64(position[1])))
}

func followWaypoint(scanner *bufio.Scanner) int {
	position := []int{0, 0}
	waypoint := []int{10, 1}

	movements := map[string][]int{
		"N": {0, 1},
		"E": {1, 0},
		"S": {0, -1},
		"W": {-1, 0},
	}

	for scanner.Scan() {
		instruction := scanner.Text()
		action := string(instruction[0])
		value, _ := strconv.Atoi(instruction[1:])

		switch action {
		case "N", "S", "E", "W":
			waypoint[0] += movements[action][0] * value
			waypoint[1] += movements[action][1] * value
			break
		case "F":
			position[0] += waypoint[0] * value
			position[1] += waypoint[1] * value
			break
		case "L", "R":
			if action == "L" {
				value *= -1
			}

			if value == 90 || value == -270 {
				// R90(x, y) = (y, -x)
				waypoint = []int{waypoint[1], waypoint[0] * -1}
			}

			if value == -90 || value == 270 {
				// R-90(x, y) = (-y, x)
				waypoint = []int{waypoint[1] * -1, waypoint[0]}
			}

			if value == 180 || value == -180 {
				// R180(x, y) = (-x, -y)
				waypoint = []int{waypoint[0] * -1, waypoint[1] * -1}
			}
			break
		}
	}

	return int(math.Abs(float64(position[0])) + math.Abs(float64(position[1])))
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day12/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := getManhattanDistance(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day12/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := followWaypoint(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
