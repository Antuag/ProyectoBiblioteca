class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, element):
        self.items.append(element)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

    def front(self):
        if self.is_empty():
            return None
        return self.items[0]

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)
