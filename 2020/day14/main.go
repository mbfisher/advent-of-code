package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func sumValues(scanner *bufio.Scanner) int64 {
	var mask map[int]string
	memory := make(map[string]int64)

	setMaskPattern := regexp.MustCompile("^mask = ([01X]+)$")
	operationPattern := regexp.MustCompile("^mem\\[([0-9]+)\\] = ([0-9]+)$")

	for scanner.Scan() {
		line := scanner.Text()

		if match := setMaskPattern.FindStringSubmatch(line); len(match) > 0 {
			mask = make(map[int]string)
			for i, bit := range match[1] {
				if string(bit) == "X" {
					continue
				}
				mask[i] = string(bit)
			}

			continue
		}

		match := operationPattern.FindStringSubmatch(line)
		address := match[1]

		valueInt, _ := strconv.Atoi(match[2])
		valueBin := fmt.Sprintf("%036b", valueInt)

		valueMasked := valueBin
		for i, bit := range mask {
			valueMasked = valueMasked[:i] + bit + valueMasked[i+1:]
		}

		maskedInt, _ := strconv.ParseInt(valueMasked, 2, 64)
		memory[address] = maskedInt
	}

	result := int64(0)
	for _, value := range memory {
		result += value
	}
	return result
}

func Part1() int64 {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day14/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := sumValues(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
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
