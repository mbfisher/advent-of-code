package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func countGroup(members []string) int {
	questions := make(map[rune]bool)

	for _, answers := range members {
		for _, q := range answers {
			questions[q] = true
		}
	}

	return len(questions)
}

func Part1() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day6/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	var group []string
	result := 0

	for scanner.Scan() {
		line := scanner.Text()

		if group == nil {
			group = []string{}
		}

		if line == "" {
			result += countGroup(group)
			group = nil
		} else {
			group = append(group, line)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	result += countGroup(group)

	fmt.Println(result)
}

func Part2() {
}


func main() {
	Part1()
	Part2()
}
