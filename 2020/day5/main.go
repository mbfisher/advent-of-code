package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
)

func getRow(spec string) int {
	row := 127

	for i := 0; i < 7; i++ {
		region := math.Pow(2, float64(7 - i)) - 1
		if string(spec[i]) == "F" {
			row -= int(math.Floor(region / 2)) + 1
		}
	}

	return row
}

func getCol(spec string) int {
	col := 7

	for i := 0; i < 3; i++ {
		region := math.Pow(2, float64(3 - i)) - 1
		if string(spec[i]) == "L" {
			col -= int(math.Floor(region / 2)) + 1
		}
	}

	return col
}

func getSeatID(spec string) int {
	rowSpec := spec[:7]
	colSpec := spec[7:]

	return getRow(rowSpec) * 8 + getCol(colSpec)
}

func Part1() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day5/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	max := 0
	for scanner.Scan() {
		id := getSeatID(scanner.Text())

		if id > max {
			max = id
		}

		fmt.Println(id)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println(max)
}

func Part2() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day5/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	seats := make(map[int]bool)
	min := 999
	max := 0
	for scanner.Scan() {
		id := getSeatID(scanner.Text())
		seats[id] = true

		if id > max {
			max = id
		}

		if id < min {
			min = id
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	for id := min; id < max; id++ {
		_, a := seats[id - 1]
		_, b := seats[id]
		c, _ := seats[id + 1]
		if a && !b && c {
			fmt.Println(id)
		}
	}
}


func main() {
	//Part1()
	Part2()
}
