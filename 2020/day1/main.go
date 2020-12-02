package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day1/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	var numbers []int

	for scanner.Scan() {
		n, _ := strconv.Atoi(scanner.Text())
		numbers = append(numbers, n)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	for i := 0; i < len(numbers); i++ {
		a := numbers[i]
		for j := i; j < len(numbers); j++ {
			b := numbers[j]

			if a + b == 2020 {
				fmt.Println(a)
				fmt.Println(b)
				fmt.Println(a * b)
			}
		}
	}
}
