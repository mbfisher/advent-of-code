package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Field struct {
	Name string
	ranges [][]int
}

func (f Field) Validate(value int) bool {
	for _, r := range f.ranges {
		if value >= r[0] && value <= r[1] {
			return true
		}
	}

	return false
}

type Input struct {
	Fields []Field
	MyTicket []int
	NearbyTickets [][]int
}

func parseTicket(line string) []int {
	var ticket []int
	for _, str := range strings.Split(line, ",") {
		value, _ := strconv.Atoi(str)
		ticket = append(ticket, value)
	}

	return ticket
}

func parse(scanner *bufio.Scanner) Input {
	lineType := "field"
	fieldRangePattern := regexp.MustCompile("(\\d+)-(\\d+)")
	input := Input{}

	for scanner.Scan() {
		line := scanner.Text()

		if line == "" {
			continue
		}

		if line == "your ticket:" {
			lineType = line
			continue
		}

		if line == "nearby tickets:" {
			lineType = line
			continue
		}

		if lineType == "field" {
			parts := strings.Split(line, ": ")
			name := parts[0]
			field := Field{Name: name}

			match := fieldRangePattern.FindAllStringSubmatch(parts[1], -1)
			for _, m := range match {
				from, _ := strconv.Atoi(m[1])
				to, _ := strconv.Atoi(m[2])
				field.ranges = append(field.ranges, []int{from, to})
			}

			input.Fields = append(input.Fields, field)
			continue
		}

		if lineType == "your ticket:" {
			input.MyTicket = parseTicket(line)
			continue
		}

		if lineType == "nearby tickets:" {
			input.NearbyTickets = append(input.NearbyTickets, parseTicket(line))
			continue
		}
	}

	return input
}

func getTicketScanningErrorRate(input Input) int {
	result := 0

	for _, ticket := range input.NearbyTickets {
		for _, value := range ticket {
			valid := false
			for _, field := range input.Fields {
				if field.Validate(value) {
					valid = true
					break
				}
			}

			if !valid {
				result += value
			}
		}
	}

	return result
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day16/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := getTicketScanningErrorRate(parse(scanner))

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day16/input.txt")
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
