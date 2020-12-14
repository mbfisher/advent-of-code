package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

func getFirstDepartureAfterTimestamp(timestamp int64, bus int) int64 {
	d := int64(math.Ceil(float64(timestamp) / float64(bus)))
	return int64(bus) * d
}

func findEarliestBus(input string) int {
	lines := strings.Split(input, "\n")
	ts, _ := strconv.Atoi(lines[0])
	timestamp := int64(ts)

	var buses []int
	for _, id := range strings.Split(lines[1], ",") {
		if id == "x" {
			continue
		}
		num, _ := strconv.Atoi(id)
		buses = append(buses, num)
	}

	min := timestamp * 2
	var bus int
	for _, id := range buses {
		next := getFirstDepartureAfterTimestamp(timestamp, id)
		if next < min {
			min = next
			bus = id
		}
	}

	return bus * int(min - timestamp)
}

func mmi(y int64, n int64) int64 {
	var z int64
	for i := int64(0); i < n; i++ {
		if (y * i) % n == 1 {
			z = i
			break
		}
	}
	return z
}

func findWeirdTimestamp(input string) int64 {
	lines := strings.Split(input, "\n")

	buses := make(map[int64]int64)
	for i, id := range strings.Split(lines[1], ",") {
		if id == "x" {
			continue
		}
		num, _ := strconv.Atoi(id)
		buses[int64(i + 1)] = int64(num)
	}

	// https://brilliant.org/wiki/chinese-remainder-theorem/
	// x ≡ pos (mod id)
	N := int64(1)
	for _, n := range buses {
		N *= n
	}

	result := int64(0)
	for n, a := range buses {
		y := N/n
		z := mmi(y, n)
		result += a * y * z
	}

	return result
}


func Part1() int {
	wd, _ := os.Getwd()
	dat, err := ioutil.ReadFile(wd + "/day13/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	input := string(dat)
	return findEarliestBus(input)
}

func Part2() int64 {
	wd, _ := os.Getwd()
	dat, err := ioutil.ReadFile(wd + "/day13/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	input := string(dat)
	return findWeirdTimestamp(input)
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
