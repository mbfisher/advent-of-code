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
	Name     string
	Position int
	ranges   [][]int
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
	Fields        []Field
	MyTicket      []int
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
			field := Field{
				Name:     name,
				Position: -1,
			}

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

func getInvalidValues(ticket []int, input Input) []int {
	var result []int

	for _, value := range ticket {
		valid := false
		for _, field := range input.Fields {
			if field.Validate(value) {
				valid = true
				break
			}
		}

		if !valid {
			result = append(result, value)
		}
	}

	return result
}

func getTicketScanningErrorRate(input Input) int {
	result := 0

	for _, ticket := range input.NearbyTickets {
		for _, value := range getInvalidValues(ticket, input) {
			result += value
		}
	}

	return result
}

func getFieldPositions(input Input) map[string]int {
	result := make(map[string]int)

	found := true
	iteration := 0
	for len(result) < len(input.Fields) {
		if !found {
			log.Fatal("no positions found")
		}

		iteration++
		fmt.Printf("iteration %d\n", iteration)
		found = false

		for _, field := range input.Fields {
			var candidates []int

			if _, ok := result[field.Name]; ok {
				continue
			}

			var allValid bool

			for i := 0; i < len(input.NearbyTickets[0]); i++ {
				assigned := false
				for _, position := range result {
					if position == i {
						assigned = true
					}
				}

				if assigned {
					continue
				}

				allValid = true

				for _, ticket := range input.NearbyTickets {
					value := ticket[i]
					if !field.Validate(value) {
						allValid = false
						break
					}
				}

				if allValid {
					candidates = append(candidates, i)
				}
			}

			fmt.Printf("found %d candidates for field %s: %v\n", len(candidates), field.Name, candidates)

			if len(candidates) == 1 {
				fmt.Printf("found position %d for field %s\n", candidates[0], field.Name)
				result[field.Name] = candidates[0]
				found = true
				break
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
	input := parse(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	var validTickets [][]int

	for _, ticket := range input.NearbyTickets {
		if len(getInvalidValues(ticket, input)) == 0 {
			validTickets = append(validTickets, ticket)
		}
	}

	fmt.Printf("discarding %d of %d tickets\n", len(input.NearbyTickets)-len(validTickets), len(input.NearbyTickets))
	input.NearbyTickets = validTickets
	positions := getFieldPositions(input)

	result := 1
	for name, position := range positions {
		if !strings.HasPrefix(name, "departure") {
			continue
		}

		result *= input.MyTicket[position]
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
