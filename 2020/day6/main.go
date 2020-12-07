package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func countGroupAnyone(members []string) int {
	questions := make(map[rune]bool)

	for _, answers := range members {
		for _, q := range answers {
			questions[q] = true
		}
	}

	return len(questions)
}

func countGroupEveryone(members []string) int {
	questions := make([]map[rune]bool, len(members))

	for i, answers := range members {
		questions[i] = make(map[rune]bool)
		for _, q := range answers {
			questions[i][q] = true
		}
	}

	exclusive := make(map[rune]bool)
	for _, q := range "abcdefghijklmnopqrstuvwxyz" {
		everyone := true
		for _, member := range questions {
			if _, ok := member[q]; !ok {
				everyone = false
			}
		}

		if everyone {
			exclusive[q] = true
		}
	}

	return len(exclusive)
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
			result += countGroupAnyone(group)
			group = nil
		} else {
			group = append(group, line)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	result += countGroupAnyone(group)

	fmt.Println(result)
}

func Part2() {
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
			result += countGroupEveryone(group)
			group = nil
		} else {
			group = append(group, line)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	result += countGroupEveryone(group)

	fmt.Println(result)
}


func main() {
	Part1()
	Part2()
}
