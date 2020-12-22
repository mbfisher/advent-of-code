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

func (n *Node) AddChild(value string, node *Node) *Node {
	if existing, ok := n.Children[value]; ok {
		for key, newChild := range node.Children {
			existing.AddChild(key, newChild)
		}
	} else {
		n.Children[value] = node
	}
	return node
}