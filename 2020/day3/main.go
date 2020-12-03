package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func Part1() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day3/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	// Throw away the first line
	scanner.Scan()

	x := 0
	numTrees := 0
	for scanner.Scan() {
		row := scanner.Text()
		rowLen := len(row)

		x += 3

		if x >= rowLen {
			x -= rowLen
		}

		if string(row[x]) == "#" {
			numTrees++
			fmt.Println(row[:x] + "X" + row[x+1:])
		} else {
			fmt.Println(row[:x] + "O" + row[x+1:])
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println(numTrees)
}

func CountTrees(rows []string, right int, down int) int {
	x := right
	numTrees := 0

	for y := down; y < len(rows); y += down {
		if string(rows[y][x]) == "#" {
			numTrees++
		}

		x += right

		rowLen := len(rows[y])
		if x >= rowLen {
			x -= rowLen
		}
	}

	return numTrees
}

func Part2() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day3/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	var rows []string

	for scanner.Scan() {
		rows = append(rows, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	a := CountTrees(rows, 1, 1)
	b := CountTrees(rows, 3, 1)
	c := CountTrees(rows, 5, 1)
	d := CountTrees(rows, 7, 1)
	e := CountTrees(rows, 1, 2)

	fmt.Println(a * b * c * d * e)
}

func main() {
	//Part1()
	Part2()
}