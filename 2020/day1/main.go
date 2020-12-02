package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func ReadInput() ([]int, error) {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day1/input.txt")
	if err != nil {
		return nil, err
	}

	scanner := bufio.NewScanner(file)
	var numbers []int

	for scanner.Scan() {
		n, _ := strconv.Atoi(scanner.Text())
		numbers = append(numbers, n)
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return numbers, nil
}

func Part1() {
	numbers, err := ReadInput()
	if err != nil {
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

func Part2() {
	numbers, err := ReadInput()
	if err != nil {
		log.Fatal(err)
	}

	for i := 0; i < len(numbers); i++ {
		a := numbers[i]
		for j := i + 1; j < len(numbers); j++ {
			b := numbers[j]

			for k := j + 1; k < len(numbers); k++ {
				c := numbers[k]

				if a+b+c == 2020 {
					fmt.Println(a)
					fmt.Println(b)
					fmt.Println(c)
					fmt.Println(a * b * c)
				}
			}
		}
	}
}

func main() {
	Part1()
	Part2()
}