class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def enqueue(self, data):
        node = Node(data)

        if not self.rear:
            self.rear = node
            self.front = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1

    def dequeue(self):
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
    
    def display(self):
        elements = []
        curr = self.front
        while curr:
            elements.append(curr.data)
            curr = curr.next
        return elements
