package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func Part1() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day2/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	numValid := 0
	pattern := regexp.MustCompile("([0-9]+)-([0-9]+) ([a-z]): (.+)")

	for scanner.Scan() {
		line := scanner.Text()
		match := pattern.FindStringSubmatch(line)

		min, _ := strconv.Atoi(match[1])
		max, _ := strconv.Atoi(match[2])
		char := match[3]
		password := match[4]

		charCount := 0
		for _, r := range password {
			p := string(r)
			if p == char {
				charCount++
			}
		}

		if charCount >= min && charCount <= max {
			fmt.Println(line)
			numValid++
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println(numValid)
}

func main() {
	Part1()
}