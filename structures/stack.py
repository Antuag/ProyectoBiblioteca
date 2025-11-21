class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, element):
        self.items.append(element)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def top(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)
