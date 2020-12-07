package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strings"
)

type BagMap map[string]Bag

type Bag struct {
	Color    string
	Contains BagMap
}

var bagPattern = regexp.MustCompile("^([a-z\\s]+)bags contain")
var containsPattern = regexp.MustCompile("(\\d+) ([a-z ]+)bag")

func parseInput(scanner *bufio.Scanner) BagMap {
	bags := make(map[string]Bag)

	newBag := func(color string) Bag {
		if bag, ok := bags[color]; ok {
			return bag
		}

		bag := Bag{
			Color:    color,
			Contains: make(map[string]Bag),
		}
		bags[color] = bag
		return bag
	}

	for scanner.Scan() {
		line := scanner.Text()

		outer := bagPattern.FindStringSubmatch(line)
		contains := containsPattern.FindAllStringSubmatch(line, -1)

		color := strings.TrimSpace(outer[1])

		bag := newBag(color)

		for _, inner := range contains {
			color := strings.TrimSpace(inner[2])
			innerBag := newBag(color)
			bag.Contains[color] = innerBag
		}
	}

	return bags
}

func checkBag(bag Bag, bags BagMap, result *map[string]bool) bool {
	//if check, ok := (*result)[bag.Color]; ok {
	//	return check
	//}

	_, ok := bag.Contains["shiny gold"]

	if ok {
		//(*result)[bag.Color] = ok
		return true
	}

	for innerColor, _ := range bag.Contains {
		innerBag := bags[innerColor]
		check := checkBag(innerBag, bags, result)
		//(*result)[innerColor] = check
		if check {
			return true
		}
	}

	return false
}

func findShinyGold(bags BagMap) int {
	result := make(map[string]bool)
	for color, bag := range bags {
		if color == "shiny gold" {
			continue
		}

		result[color] = checkBag(bag, bags, &result)
	}

	numBags := 0
	for _, match := range result {
		if match {
			numBags++
		}
	}

	return numBags
}

func Part1() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day7/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	bags := parseInput(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println(findShinyGold(bags))
}

func Part2() {

}

func main() {
	Part1()
	Part2()
}
