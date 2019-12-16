package day2

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func run(input string, noun int, verb int) int {
	program := make(map[int]int)

	for position, element := range strings.Split(input, ",") {
		value, _ := strconv.Atoi(element)
		program[position] = value
	}

	program[1] = noun
	program[2] = verb

	position := 0

	for true {
		opcode := program[position]

		if opcode == 99 {
			break
		}

		a := program[program[position+1]]
		b := program[program[position+2]]
		store := program[position+3]
		var result int

		if opcode == 1 {
			result = a + b
		} else {
			result = a * b
		}

		//fmt.Printf("opcode: %d, a: %d, b: %d, store: %d, result: %d\n", opcode, a, b, store, result)
		program[store] = result

		position += 4
	}

	for i := 0; i < len(program); i++ {
		//fmt.Printf("%d,", program[i])
	}

	//fmt.Print("\n")

	return program[0]
}

func part1() {
	content, _ := ioutil.ReadFile("./day2/input.txt")
	run(string(content), 12, 2)
}

func part2() {
	content, _ := ioutil.ReadFile("./day2/input.txt")
	input := string(content)
	noun, verb := 0, 0

	for noun <= 99 {
		verb = 0
		for verb <= 99 {
			result := run(input, noun, verb)
			if result == 19690720 {
				fmt.Printf("noun: %d, verb: %d, result: %d\n", noun, verb, 100 * noun + verb)
				return
			}
			verb++
		}
		noun++
	}
}

func Day2() {
	part1()
	part2()
	//run("1,0,0,0,99")
	//run("2,3,0,3,99")
	//run("2,4,4,5,99,0")
	//run("1,1,1,4,99,5,6,0,99")
}
