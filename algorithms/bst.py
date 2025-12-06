class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BST:
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None
    
    def insert(self, data, node=None):
        if node is None:
            if self.root is None:
                self.root = Node(data)
                return self.root
            node = self.root

        if data < node.value:
            if node.left is None:
                node.left = Node(data)
            else:
                self.insert(data, node.left)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self.insert(data, node.right)
        return node
    
    def search(self, target, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        
        if node.value == target:
            return node
        
        elif target < node.value:
            if node.left is None:
                return None
            return self.search(target, node.left)
        else:
            if node.right is None:
                return None
            return self.search(target, node.right)
    
    def get_min(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        
        current = node
        while current.left:
            current = current.left
        return current.value

    def get_max(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        
        current = node
        while current.right:
            current = current.right
        return current.value
    
    def find_height(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return -1

        if node.left is None and node.right is None:
            return 0

        left_height = self.find_height(node.left) if node.left else -1
        right_height = self.find_height(node.right) if node.right else -1
        return 1 + max(left_height, right_height)
    
    def get_min_node(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        
        current = node
        while current.left:
            current = current.left
        return current
    
    def delete(self, value, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None

        if value < node.value:
            node.left = self.delete(value, node.left)
        elif value > node.value:
            node.right = self.delete(value, node.right)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Find inorder successor
                succ = self.get_min_node(node.right)
                node.value = succ.value
                node.right = self.delete(succ.value, node.right)
        return node

    def preorder_traversal(self, start, traversal=""):
        if start:
            traversal += (str(start.value) + " ")
            traversal = self.preorder_traversal(start.left, traversal)
            traversal = self.preorder_traversal(start.right, traversal)
        return traversal

    def inorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.inorder_traversal(start.left, traversal)
            traversal += (str(start.value) + " ")
            traversal = self.inorder_traversal(start.right, traversal)
        return traversal
    
    def postorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.postorder_traversal(start.left, traversal)
            traversal = self.postorder_traversal(start.right, traversal)
            traversal += str(start.value) + " "
        return traversal
