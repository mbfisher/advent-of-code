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

func version1(scanner *bufio.Scanner) int64 {
	var mask map[int]string
	memory := make(map[string]int64)

	setMaskPattern := regexp.MustCompile("^mask = ([01X]+)$")
	operationPattern := regexp.MustCompile("^mem\\[([0-9]+)\\] = ([0-9]+)$")

	for scanner.Scan() {
		line := scanner.Text()

		if match := setMaskPattern.FindStringSubmatch(line); len(match) > 0 {
			mask = make(map[int]string)
			for i, bit := range match[1] {
				if string(bit) == "X" {
					continue
				}
				mask[i] = string(bit)
			}

			continue
		}

		match := operationPattern.FindStringSubmatch(line)
		address := match[1]

		valueInt, _ := strconv.Atoi(match[2])
		valueBin := fmt.Sprintf("%036b", valueInt)

		valueMasked := valueBin
		for i, bit := range mask {
			valueMasked = valueMasked[:i] + bit + valueMasked[i+1:]
		}

		maskedInt, _ := strconv.ParseInt(valueMasked, 2, 64)
		memory[address] = maskedInt
	}

	result := int64(0)
	for _, value := range memory {
		result += value
	}
	return result
}

func setValue(address string, value int64, memory *map[int64]int64) []string {
	floatingIndex := strings.Index(address, "X")

	if floatingIndex < 0 {
		addressVal, _ := strconv.ParseInt(address, 2, 64)
		//fmt.Printf("setting %d = %d (%s)\n", addressVal, value, address)
		(*memory)[addressVal] = value
		return []string{address}
	}

	var result []string

	//fmt.Printf("replacing X at %d: %s\n", floatingIndex, address)
	result = append(result, setValue(address[:floatingIndex] + "0" + address[floatingIndex+1:], value, memory)...)
	result = append(result, setValue(address[:floatingIndex] + "1" + address[floatingIndex+1:], value, memory)...)

	return result
}

func version2(scanner *bufio.Scanner) int64 {
	var mask map[int]string
	memory := make(map[int64]int64)

	setMaskPattern := regexp.MustCompile("^mask = ([01X]+)$")
	operationPattern := regexp.MustCompile("^mem\\[([0-9]+)\\] = ([0-9]+)$")

	progress := 1
	for scanner.Scan() {
		fmt.Printf("%d\n", progress)
		progress++

		line := scanner.Text()

		if match := setMaskPattern.FindStringSubmatch(line); len(match) > 0 {
			fmt.Printf("parsing mask: %s\n", match[1])
			mask = make(map[int]string)
			for i, bit := range match[1] {
				if string(bit) == "0" {
					continue
				}

				mask[i] = string(bit)
			}

			continue
		}

		fmt.Printf("proccessing: %s\n", line)
		match := operationPattern.FindStringSubmatch(line)
		value, _ := strconv.Atoi(match[2])
		addressInt, _ := strconv.Atoi(match[1])
		addressBin := fmt.Sprintf("%036b", addressInt)

		addressMasked := addressBin
		for i, bit := range mask {
			addressMasked = addressMasked[:i] + bit + addressMasked[i+1:]
		}

		fmt.Printf("setting value: %s\n", addressMasked)
		addresses := setValue(addressMasked, int64(value), &memory)
		fmt.Printf("set %d values\n", len(addresses))
	}

	result := int64(0)
	for _, value := range memory {
		result += value
	}
	return result
}


func Part1() int64 {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day14/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := version1(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int64 {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day14/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := version2(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
