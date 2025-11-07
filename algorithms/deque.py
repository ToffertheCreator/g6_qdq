class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Deque:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def add_front(self, data):
        node = Node(data)

        if not self.front:
            self.front = node
            self.rear = node
        else:
            node.next = self.front
            self.front = node
        self.size += 1

    def add_rear(self, data):
        node = Node(data)

        if not self.rear:
            self.rear = node
            self.front = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1

    def remove_front(self):
        if not self.front:
            return
        
        removed_data = self.front.data
        if not self.front.next:
            self.front = None
            self.rear = None
        else:
            self.front = self.front.next
        self.size -= 1
        return removed_data

    def remove_rear(self):
        if not self.rear:
            return
        
        if not self.front.next:
            removed_data = self.front.data
            self.front = None
            self.rear = None
            self.size -= 1
            return removed_data
        else:
            curr = self.front
            while curr.next.next:
                curr = curr.next
            removed_data = curr.next.data
            curr.next = None
            self.rear = curr
            self.size -= 1
            return removed_data
    
    def display(self):
        elements = []
        curr = self.front
        while curr:
            elements.append(curr.data)
            curr = curr.next
        return elements