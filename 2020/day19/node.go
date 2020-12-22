package main

type Node struct {
	Children map[string]*Node
}

func NewNode() *Node {
	return &Node{Children: make(map[string]*Node)}
}

func (n *Node) Clone() (root *Node, leaves []*Node) {
	root = NewNode()

	for k, v := range n.Children {
		child, cl := v.Clone()
		root.Children[k] = child
		leaves = append(leaves, cl...)
	}

	if len(root.Children) == 0 {
		leaves = []*Node{root}
	}

	return
}

func (n *Node) AddEdge(value string) *Node {
	return n.AddChild(value, NewNode())
}

func MergeNodes(dest *Node, srcs ...*Node) {
	for _, src := range srcs {
		for key, child := range src.Children {
			if existing, ok := dest.Children[key]; ok {
				MergeNodes(existing, child)
			} else {
				dest.Children[key] = child
			}
		}
	}
}

func (n *Node) AddChild(value string, node *Node) *Node {
	n.Children[value] = node
	return node
}

func (n *Node) Leaves() (result []*Node) {
	for _, child := range n.Children {
		if len(child.Children) == 0 {
			result = append(result, child)
		} else {
			result = append(result, child.Leaves()...)
		}
	}

	return
}
