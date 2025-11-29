class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BinarySearchTree:
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None
    
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:

            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def insert_left(self, value, start=None):
        if start is None:
            start = self.root
        
        if start is None:
            return
        
        new_node = Node(value)
        new_node.left = start.left
        start.left = new_node
    
    def insert_right(self, value, start=None):
        if start is None:
            start = self.root
        
        if start is None:
            return
        
        new_node = Node(value)
        new_node.right = start.right
        start.right = new_node
    
    def find_node_by_value(self, value, start=None):
        if start is None:
            start = self.root
        if start is None:
            return None
        
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node.value == value:
                return node  
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return None
    
    def search(self, node, value):
        """Search for a value in the BST"""
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self.search(node.left, value)
        else:
            return self.search(node.right, value)
    
    def delete(self, node, value):
        if node is None:
            return None
        
        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value > node.value:
            node.right = self.delete(node.right, value)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._find_min(node.right)
                node.value = successor.value
                node.right = self.delete(node.right, successor.value)
        
        return node
    
    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def get_max_value(self, node):
        if node is None:
            return None
        current = node
        while current.right is not None:
            current = current.right
        return current.value
    
    def get_min_value(self, node):
        """
        Min Value Node Algorithm:
        1. Start at the root node of the subtree.
        2. Go left as far as possible.
        3. The node you end up in is the node with the lowest value in that BST subtree.
        """
        if node is None:
            return None
        current = node
        # Step 2: Go left as far as possible
        while current.left is not None:
            current = current.left
        # Step 3: Return the minimum value found
        return current.value
    
    def find_height(self, node):
        if node is None:
            return 0
        left_height = self.find_height(node.left)
        right_height = self.find_height(node.right)
        return 1 + max(left_height, right_height)
    
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
    
    def post_traversal(self, start, traversal=""):
        return self.postorder_traversal(start, traversal)