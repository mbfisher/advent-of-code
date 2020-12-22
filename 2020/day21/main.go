package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Recipe struct {
	ID          string
	Ingredients Set
	Allergens   Set
}

type Allergens map[string]string
type AllAllergens map[string][]Recipe
type AllIngredients map[string][]Recipe

func parse(scanner *bufio.Scanner) (recipes []Recipe, ingredients AllIngredients, allergens Allergens) {
	allAllergens := make(AllAllergens)
	ingredients = make(AllIngredients)
	id := 0
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(strings.Trim(line, ")"), " (contains ")
		recipe := Recipe{
			ID:          strconv.Itoa(id),
			Ingredients: set(strings.Split(parts[0], " ")),
			Allergens:   set(strings.Split(parts[1], ", ")),
		}
		recipes = append(recipes, recipe)

		for allergen := range recipe.Allergens {
			allAllergens[allergen] = append(allAllergens[allergen], recipe)
		}
		for ingredient := range recipe.Ingredients {
			ingredients[ingredient] = append(ingredients[ingredient], recipe)
		}

		id++
	}

	allergens = resolveAllergens(allAllergens)
	for allergen, ingredient := range allergens {
		for _, recipe := range ingredients[ingredient] {
			recipe.Allergens.Add(allergen)
		}
	}

	return
}

type Set map[string]bool

func emptySet() Set {
	return make(Set)
}

func set(items []string) Set {
	result := make(Set)
	for _, item := range items {
		result[item] = true
	}
	return result
}

func (s Set) Add(item string) {
	s[item] = true
}

func (s Set) Remove(item string) {
	delete(s, item)
}

func (s Set) Intersection(b Set) Set {
	result := make(Set)
	for k := range s {
		if _, ok := b[k]; ok {
			result[k] = true
		}
	}
	for k := range b {
		if _, ok := s[k]; ok {
			result[k] = true
		}
	}
	return result
}

func (s Set) Equals(b Set) bool {
	if len(s) != len(b) {
		return false
	}

	for item := range s {
		if _, ok := b[item]; !ok {
			return false
		}
	}

	return true
}

func (s Set) Clone() Set {
	result := make(Set)
	for item := range s {
		result[item] = true
	}
	return result
}

func (s Set) Slice() []string {
	var result []string
	for item := range s {
		result = append(result, item)
	}
	return result
}

func resolveAllergens(allergens AllAllergens) Allergens {
	// Get a set of ingredients that is marked with each allergen
	allergenOccurrences := make(map[string]Set)
	for allergen, recipes := range allergens {
		ingSet := recipes[0].Ingredients
		for _, recipe := range recipes {
			ingSet = ingSet.Intersection(recipe.Ingredients)
		}
		allergenOccurrences[allergen] = ingSet
	}

	result := make(map[string]string)

	for len(result) < len(allergens) {
		for allergen, ingredients := range allergenOccurrences {
			if len(ingredients) == 1 {
				ing := ingredients.Slice()[0]
				result[ing] = allergen

				for _, occurrences := range allergenOccurrences {
					occurrences.Remove(ing)
				}
			}
		}
	}

	return result
}

func noAllergens(allergens Allergens, ingredients AllIngredients) Set {
	result := emptySet()

	for ingredient := range ingredients {
		if _, ok := allergens[ingredient]; !ok {
			result.Add(ingredient)
		}
	}

	return result
}

func part1(scanner *bufio.Scanner) int {
	_, ingredients, allergens := parse(scanner)

	result := 0
	for ingredient := range noAllergens(allergens, ingredients) {
		result += len(ingredients[ingredient])
	}

	return result
}

func part2(scanner *bufio.Scanner) string {
	_, _, allergens := parse(scanner)

	var ingredientsList []string
	for ingredient := range allergens {
		ingredientsList = append(ingredientsList, ingredient)
	}

	sort.Slice(ingredientsList, func (a, b int) bool {
		return allergens[ingredientsList[a]] < allergens[ingredientsList[b]]
	})

	return strings.Join(ingredientsList, ",")
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day21/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := part1(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() string {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day21/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := part2(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
