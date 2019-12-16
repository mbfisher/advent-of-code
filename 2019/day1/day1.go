package day1

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
)

func fuelForMass(mass float64) float64 {
	fuel := math.Floor(mass / 3) - 2
	//fmt.Printf("mass: %.2f, fuel: %.2f\n", mass, fuel)
	return fuel
}

func part1() {
	file, _ := os.Open("./day1/input.txt")
	scanner := bufio.NewScanner(file)

	var total float64 = 0
	for scanner.Scan() {
		mass, _ := strconv.Atoi(scanner.Text())
		total += fuelForMass(float64(mass))
	}

	fmt.Printf("%.2f\n", total)
}

func part2() {
	file, _ := os.Open("./day1/input.txt")
	scanner := bufio.NewScanner(file)

	var total float64 = 0
	var extra float64

	for scanner.Scan() {
		mass, _ := strconv.Atoi(scanner.Text())
		fuel := fuelForMass(float64(mass))
		extra = fuel

		for true {
			extra = fuelForMass(extra)
			if extra > 0 {
				fuel += extra
			} else {
				break
			}
		}

		total += fuel
	}

	fmt.Printf("%.2f\n", total)
}

func Day1() {
	part1()
	part2()
}
