package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func parse(scanner *bufio.Scanner) (seats [][]string) {
	for scanner.Scan() {
		line := scanner.Text()
		var row []string
		for _, seat := range line {
			row = append(row, string(seat))
		}
		seats = append(seats, row)
	}

	return
}

func stringify(seats [][]string) (result string) {
	for row := 0; row < len(seats); row++ {
		for col := 0; col < len(seats[row]); col++ {
			result += seats[row][col]
		}
		result += "\n"
	}

	return
}

func doRound(seats [][]string, distance int, threshold int) (next [][]string) {
	numRows := len(seats)
	numCols := len(seats[0])

	next = make([][]string, numRows)

	directions := [][]int{
		{-1, 0}, // N
		{-1, 1}, // NE
		{0, 1}, // E
		{1, 1}, // SE
		{1, 0}, // S
		{1, -1}, // SW
		{0, -1}, // W
		{-1, -1}, // NW
	}

	visitAdjacent := func(row int, col int, visitor func(seat string) bool) {
		for _, steps := range directions {
			x := steps[0]
			y := steps[1]

			i := row
			j := col

			seat := "."
			n := 0
			for seat == "." {
				n++
				if distance > 0 && n > distance {
					break
				}

				i += x
				j += y

				if i < 0 || i >= numRows {
					break
				}

				if j < 0 || j >= numCols {
					break
				}

				seat = seats[i][j]
			}

			if seat == "." {
				continue
			}

			if !visitor(seat) {
				return
			}
		}
	}

	shouldOccupy := func(row int, col int) bool {
		result := true
		visitAdjacent(row, col, func(seat string) bool {
			if seat == "." {
				return true
			}
			result = seat != "#"
			return result
		})

		return result
	}

	shouldEmpty := func (row int, col int) bool {
		numOccupied := 0
		visitAdjacent(row, col, func(seat string) bool {
			if seat == "#" {
				numOccupied++
			}

			return numOccupied < threshold
		})

		return numOccupied >= threshold
	}

	for row := 0; row < numRows; row++ {
		next[row] = make([]string, numCols)

		for col := 0; col < numCols; col++ {
			next[row][col] = seats[row][col]
			if seats[row][col] == "L" && shouldOccupy(row, col) {
				next[row][col] = "#"
			} else if seats[row][col] == "#" && shouldEmpty(row, col) {
				next[row][col] = "L"
			}
		}
	}

	return next
}

func countOccupied(scanner *bufio.Scanner, distance int, threshold int) int {
	var seats [][]string

	for scanner.Scan() {
		line := scanner.Text()
		var row []string
		for _, seat := range line {
			row = append(row, string(seat))
		}
		seats = append(seats, row)
	}

	previousHash := "start"
	currentHash := ""
	numRounds := 0
	next := seats
	for previousHash != currentHash {
		previousHash = currentHash

		numRounds++
		fmt.Printf("Round %d\n", numRounds)

		next = doRound(next, distance, threshold)
		currentHash = stringify(next)
	}

	result := 0

	for row := 0; row < len(next); row++ {
		for col := 0; col < len(next[row]); col++ {
			if next[row][col] == "#" {
				result++
			}
		}
	}

	return result
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day11/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := countOccupied(scanner, 1, 4)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day11/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := countOccupied(scanner, -1, 5)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
