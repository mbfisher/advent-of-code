package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func Evaluate(expression string) int {
	result := -1
	var operator string

	for i := 0; i < len(expression); i++ {
		char := string(expression[i])

		if char == " " {
			continue
		}

		if char == "*" || char == "+" {
			operator = char
			continue
		}

		var num int
		var err error

		if char == "(" {
			sub := ""
			var stack []string
			for j := i + 1; j < len(expression); j++ {
				next := string(expression[j])

				if next == "(" {
					stack = append(stack, next)
				}

				if next == ")" {
					if len(stack) == 0 {
						num = Evaluate(sub)
						i = j + 1
						break
					} else {
						stack = stack[:len(stack)-1]
					}
				}

				sub += next
			}
		} else {
			num, err = strconv.Atoi(char)
			if err != nil {
				panic(fmt.Sprintf("failed to parse char %s", char))
			}
		}

		if result == -1 {
			result = num
			continue
		}

		if operator == "*" {
			result *= num
		} else {
			result += num
		}
	}

	return result
}

func Advanced(expression string) int {
	result := -1

	exp := expression

	for strings.Contains(exp, "(") {
		for i := 0; i < len(exp); i++ {
			char := string(exp[i])

			if char != "(" {
				continue
			}

			sub := ""
			var stack []string
			for j := i + 1; j < len(exp); j++ {
				next := string(exp[j])

				if next == "(" {
					stack = append(stack, next)
				}

				if next == ")" {
					if len(stack) == 0 {
						num := Advanced(sub)
						exp = exp[:i] + strconv.Itoa(num) + exp[j+1:]
						break
					} else {
						stack = stack[:len(stack)-1]
					}
				}

				sub += next
			}

			break
		}
	}

	if strings.Contains(exp, "*") {
		result = 1
		for _, sub := range strings.Split(exp, " * ") {
			result *= Advanced(sub)
		}
		return result
	}

	if strings.Contains(exp, "+") {
		result = 0
		for _, char := range strings.Split(exp, " + ") {
			num, _ := strconv.Atoi(char)
			result += num
		}
		return result
	}

	num, err := strconv.Atoi(exp)
	if err != nil {
		panic(fmt.Sprintf("failed to evaluate %s", exp))
	}

	return num
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day18/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	result := 0
	for scanner.Scan() {
		result += Evaluate(scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day18/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	result := 0
	for scanner.Scan() {
		result += Advanced(scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
