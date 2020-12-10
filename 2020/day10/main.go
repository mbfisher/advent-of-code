package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)

func findJoltDifferenceProduct(scanner *bufio.Scanner) int {
	jolts := []int{0}

	for scanner.Scan() {
		val, _ := strconv.Atoi(scanner.Text())
		jolts = append(jolts, val)
	}

	sort.Slice(jolts, func(i, j int) bool {
		return jolts[i] < jolts[j]
	})

	jolts = append(jolts, jolts[len(jolts)-1]+3)

	result := map[int]int{
		1: 0,
		3: 0,
	}

	for i := 1; i < len(jolts); i++ {
		diff := jolts[i] - jolts[i-1]
		if diff == 1 {
			result[1]++
		}
		if diff == 3 {
			result[3]++
		}
	}

	return result[1] * result[3]
}

func countCombos(start int, jolts *map[int]int) (result int) {
	if start == 0 {
		return 1
	}

	if hops, ok := (*jolts)[start]; ok && hops > 0 {
		return hops
	}

	result = 0
	for _, d := range []int{3, 2, 1} {
		next := start - d

		if _, ok := (*jolts)[next]; ok {
			result += countCombos(next, jolts)
		}
	}

	(*jolts)[start] = result

	return
}

func findCombinations(scanner *bufio.Scanner) int {
	jolts := make(map[int]int)
	jolts[0] = 0
	builtIn := 0

	for scanner.Scan() {
		val, _ := strconv.Atoi(scanner.Text())
		jolts[val] = 0
		if val > builtIn {
			builtIn = val
		}
	}

	result := countCombos(builtIn , &jolts)

	return result
	
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day10/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	result := findJoltDifferenceProduct(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day10/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	result := findCombinations(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
