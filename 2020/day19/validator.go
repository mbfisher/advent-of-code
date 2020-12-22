package main

import "fmt"

type Validator struct {
	tree *Node
}

type ValidationResult struct {
	IsValid bool
	Message string
}

func (v *Validator) Validate(message string) (result ValidationResult) {
	node := v.tree
	for i, r := range message {
		c := string(r)

		if len(node.Children) == 0 {
			if node.Recurse != nil {
				node = node.Recurse
				if child, ok := node.Children[c]; ok {
					node = child
					continue
				} else {
					return ValidationResult{
						IsValid: false,
						Message: fmt.Sprintf("invalid char %d %s", i, c),
					}
				}
			} else {
				return ValidationResult{
					IsValid: false,
					Message: fmt.Sprintf("too long"),
				}
			}
		}

		if child, ok := node.Children[c]; ok {
			node = child
			continue
		} else {
			if node.Recurse != nil {
				node = node.Recurse
				if child, ok := node.Children[c]; ok {
					node = child
					continue
				} else {
					return ValidationResult{
						IsValid: false,
						Message: fmt.Sprintf("invalid char %d %s", i, c),
					}
				}
			} else {
				return ValidationResult{
					IsValid: false,
					Message: fmt.Sprintf("invalid char %d %s", i, c),
				}
			}
		}
	}

	if len(node.Children) > 0 {
		return ValidationResult{
			IsValid: false,
			Message: "too short",
		}
	}
	
	if node.Recurse != nil {
		return ValidationResult{
			IsValid: false,
			Message: "ended mid-cycle",
		}
	}

	return ValidationResult{
		IsValid: true,
	}
}
