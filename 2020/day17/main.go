package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

type Slice map[int]map[int]bool
type State map[int]Slice

func boot(input string, cycles int) State {
	initial := make(map[int]map[int]bool)
	for y, line := range strings.Split(input, "\n") {
		row := make(map[int]bool)

		for x, char := range line {
			var state bool
			if string(char) == "#" {
				state = true
			}

			row[x] = state
		}

		initial[y] = row
	}

	state := make(State)
	state[0] = initial
	Y := len(initial)
	X := len(initial[0])


	for i := 1; i <= cycles; i++ {
		iteration := make(State)
		var delta [][]int

		for z, _ := range state {
			iteration[z] = make(Slice)
			for y, _ := range state[z] {
				iteration[z][y] = make(map[int]bool)
				for x, _ := range state[z][y] {
					iteration[z][y][x] = state[z][y][x]
				}
			}
		}

		b := i + Y
		c := i + X

		for z := i * -1; z <= i; z++ {
			for y := 3 - b; y < b; y++ {
				for x := 3 - c; x < c; x++ {
					//fmt.Printf("cube (%d, %d, %d)\n", z, y, x)
					if _, ok := iteration[z]; !ok {
						iteration[z] = make(Slice)
					}

					if _, ok := iteration[z][y]; !ok {
						iteration[z][y] = make(map[int]bool)
					}

					if _, ok := iteration[z][y][x]; !ok {
						iteration[z][y][x] = false
					}

					cube := iteration[z][y][x]
					activeNeighbours := 0

					for j := z - 1; j <= z+1; j++ {
						for k := y - 1; k <= y+1; k++ {
							for l := x - 1; l <= x+1; l++ {
								if j == z && k == y && l == x {
									continue
								}

								cube, ok := iteration[j][k][l]

								if !ok {
									continue
								}

								//fmt.Printf("neighbour (%d, %d, %d)\n", j, k, l)

								if cube {
									activeNeighbours++
								}
							}
						}
					}

					//fmt.Printf("%v (%d, %d, %d) %d\n", cube, z, y, x, activeNeighbours)

					if cube && activeNeighbours != 2 && activeNeighbours != 3 {
						//fmt.Printf("deactivating (%d, %d, %d)\n", z, y, x)
						delta = append(delta, []int{z, y, x, 0})
					}

					if !cube && activeNeighbours == 3 {
						//fmt.Printf("activating (%d, %d, %d)\n", z, y, x)
						delta = append(delta, []int{z, y, x, 1})
					}
				}
			}
		}

		for _, d := range delta {
			z, y, x, v := d[0], d[1], d[2], d[3]
			iteration[z][y][x] = v == 1
		}

		state = iteration
	}

	return state
}

func countActive(state State) int {
	result := 0
	for z, _ := range state {
		for y, _ := range state[z] {
			for x, _ := range state[z][y] {
				if state[z][y][x] {
					result++
				}
			}
		}
	}

	return result
}

func Part1() int {
	wd, _ := os.Getwd()
	data, err := ioutil.ReadFile(wd + "/day17/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	result := countActive(boot(string(data), 6))

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day17/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := 0

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	fmt.Println(Part1())
	//fmt.Println(Part2())
}
