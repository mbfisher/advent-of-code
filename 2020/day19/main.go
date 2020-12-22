package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day19/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := 0

	tree, messages := Parse(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	validator := Validator{tree}

	for _, message := range messages {
		if validationResult := validator.Validate(message); validationResult.IsValid {
			result++
			fmt.Printf("%s: ✅\n", message)
		} else {
			fmt.Printf("%s: %s\n", message, validationResult.Message)
		}
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day19/input.txt")
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
