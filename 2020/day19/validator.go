package main

import "fmt"

type Validator struct {
	tree *Node
}

type ValidationResult struct {
	IsValid bool
	Message string
}

func (v *Validator) Validate(message string) ValidationResult {
	node := v.tree
	for i, r := range message {
		c := string(r)
		//if len(node.Children) == 0 {
		//	return false
		//}

		if child, ok := node.Children[c]; ok {
			node = child
		} else {
			return ValidationResult{
				IsValid: false,
				Message: fmt.Sprintf("invalid char %d %s", i, c),
			}
		}
	}

	return ValidationResult{
		IsValid: true,
	}
}
