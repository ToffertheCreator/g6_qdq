class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None
    
    def insert_left(self, value, start=None):
        if start is None:
            start = self.root
        
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node.left is None:
                node.left = Node(value)
                return
            else:
                queue.append(node.left)

            if node.right is None:
                node.right = Node(value)
                return
            else:
                queue.append(node.right)
    
    def insert_right(self, value, start=None):
        if start is None:
            start = self.root
        
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node.right is None:
                node.right = Node(value)
                return
            else:
                queue.append(node.right)

            if node.left is None:
                node.left = Node(value)
                return
            else:
                queue.append(node.left)
    
    def find_node_by_value(self, value, start=None):
        if start is None:
            start = self.root
        if start is None:
            return None
        
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node.value == value:
                return node  # returns the first matching node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return None
    
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

    def delete(self, value):
        if self.root is None:
            return False
        
        if self.root.value == value:
            # If root is to be deleted
            if self.root.left is None and self.root.right is None:
                self.root = None
                return True
            elif self.root.left is None:
                self.root = self.root.right
                return True
            elif self.root.right is None:
                self.root = self.root.left
                return True
            else:
                # Find inorder successor (leftmost node in right subtree)
                parent = self.root
                successor = self.root.right
                while successor.left is not None:
                    parent = successor
                    successor = successor.left
                
                # Replace root value with successor value
                self.root.value = successor.value
                
                # Delete successor
                if parent == self.root:
                    self.root.right = successor.right
                else:
                    parent.left = successor.right
                return True
        
        # For non-root nodes, use BFS to find and delete
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            
            # Check left child
            if node.left and node.left.value == value:
                if node.left.left is None and node.left.right is None:
                    node.left = None
                elif node.left.left is None:
                    node.left = node.left.right
                elif node.left.right is None:
                    node.left = node.left.left
                else:
                    # Find inorder successor
                    parent = node.left
                    successor = node.left.right
                    while successor.left is not None:
                        parent = successor
                        successor = successor.left
                    
                    node.left.value = successor.value
                    if parent == node.left:
                        node.left.right = successor.right
                    else:
                        parent.left = successor.right
                return True
            
            # Check right child
            if node.right and node.right.value == value:
                if node.right.left is None and node.right.right is None:
                    node.right = None
                elif node.right.left is None:
                    node.right = node.right.right
                elif node.right.right is None:
                    node.right = node.right.left
                else:
                    # Find inorder successor
                    parent = node.right
                    successor = node.right.right
                    while successor.left is not None:
                        parent = successor
                        successor = successor.left
                    
                    node.right.value = successor.value
                    if parent == node.right:
                        node.right.right = successor.right
                    else:
                        parent.left = successor.right
                return True
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return False
    
    def search(self, value, start=None):
        if start is None:
            start = self.root
        if start is None:
            return False
        
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node.value == value:
                return True
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return False
