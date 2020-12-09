package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func findFirstBad(scanner *bufio.Scanner, preamble int) int {
	var queue []int

	hasSum := func(num int) bool {
		for i := 0; i < len(queue); i++ {
			for j := i; j < len(queue); j++ {
				if queue[i] != queue[j] && queue[i] + queue[j] == num {
					return true
				}
			}
		}

		return false
	}

	for scanner.Scan() {
		num, _ := strconv.Atoi(scanner.Text())

		if len(queue) < preamble {
			queue = append(queue, num)
			continue
		}

		if !hasSum(num) {
			return num
		}

		queue = append(queue[1:], num)
	}

	return 0
}

func findWeakness(scanner *bufio.Scanner, invalidNum int) int {
	var numbers []int

	for scanner.Scan() {
		num, _ := strconv.Atoi(scanner.Text())
		numbers = append(numbers, num)
	}

	var conRange []int

	for i := 0; i < len(numbers); i++ {
		if conRange != nil {
			break
		}

		for j := i; j < len(numbers); j++ {
			sum := 0

			for k := i; k < j; k++ {
				sum += numbers[k]
			}

			if sum == invalidNum {
				conRange = numbers[i:j]
				break
			}
		}
	}

	min := 0
	max := 0

	for _, c := range conRange {
		if c < min || min == 0 {
			min = c
		}

		if c > max {
			max = c
		}
	}

	return max + min
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day9/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	result := findFirstBad(scanner, 25)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day9/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	result := findWeakness(scanner, 138879426)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	fmt.Println(Part1())
	fmt.Println(Part2())
}
