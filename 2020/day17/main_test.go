package main

import (
	"fmt"
	"log"
	"testing"
)

func debug(input string, cycles int) {
	for i := 1; i<=cycles; i++ {
		state := boot(input, cycles)

		b := i + 3
		for z := i * -1; z <= i; z++ {
			fmt.Printf("z=%d\n", z)
			for y := 3 - b; y < b; y++ {
				line := ""
				for x := 3 - b; x < b; x++ {
					cube, ok := state[z][y][x]
					if !ok {
						log.Fatalf("invalid coord (%d, %d, %d)", z, y, x)
					}

					if cube {
						line += "#"
					} else {
						line += "."
					}
				}
				fmt.Println(line)
			}

			fmt.Println()
		}

		fmt.Print("---------------\n\n")
	}
}

func TestBoot(t *testing.T) {
	initialState := `.#.
..#
###`

	debug(initialState, 3)
	state := boot(initialState, 6)
	result := countActive(state)
	if result != 112 {
		t.Fatalf("got %d want 112", result)
	}
}
