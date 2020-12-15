package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func nthSpoken(input string, n int) int {
	memory := make(map[int][]int)
	current := 0
	start := 1
	for _, str := range strings.Split(input, ",") {
		number, _ := strconv.Atoi(str)
		memory[number] = []int{start}
		current = number
		start++
	}

	first := true
	for i := start; i <= n; i++ {
		if first {
			current = 0
		} else {
			spoken := memory[current]
			current = spoken[1] - spoken[0]
		}

		if spoken, ok := memory[current]; ok {
			first = false

			if len(spoken) == 2 {
				memory[current] = []int{memory[current][1], i}
			} else {
				memory[current] = []int{memory[current][0], i}
			}
		} else {
			first = true
			memory[current] = []int{i}
		}
	}

	return current
}

func Part1() int {
	input := "0,1,5,10,3,12,19"
	return nthSpoken(input, 2020)
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day14/input.txt")
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
