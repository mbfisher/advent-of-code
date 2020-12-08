package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func runProgram(code []string) (accumulator int, finished bool) {
	visited := make(map[int]bool)

	i := 0
	for true {
		if visited[i] {
			break
		}

		if i >= len(code) {
			finished = true
			break
		}

		line := code[i]
		visited[i] = true

		parts := strings.Split(line, " ")
		operation := parts[0]
		argument, _ := strconv.Atoi(parts[1])

		switch operation {
		case "acc":
			accumulator += argument
			i++
		case "jmp":
			i += argument
		case "nop":
			i++
		}
	}

	return
}

func fixProgram(code []string) int {
	for l, line := range code {
		parts := strings.Split(line, " ")
		operation := parts[0]
		argument, _ := strconv.Atoi(parts[1])

		if operation == "nop" || operation == "jmp" {
			fixedCode := make([]string, len(code))
			copy(fixedCode, code)

			if operation == "nop" {
				fixedCode[l] = fmt.Sprintf("jmp %d", argument)
			}

			if operation == "jmp" {
				fixedCode[l] = fmt.Sprintf("nop %d", argument)
			}

			if result, finished := runProgram(fixedCode); finished {
				return result
			}

		}
	}

	return 0
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day8/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	var code []string
	for scanner.Scan() {
		code = append(code, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	result, _ := runProgram(code)
	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day8/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	var code []string
	for scanner.Scan() {
		code = append(code, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return fixProgram(code)
}

func main() {
	fmt.Println(Part1())
	fmt.Println(Part2())
}
