from structures.queue import Queue
class Book:
    
    def __init__(self,isbn,title,author,weight,value,stock=1):
        
        self.isbn = str(isbn)
        self.title = title
        self.author = author
        self.weight = float(weight)
        self.value = int(value)
        self.stock = int(stock)
        self.reservations = Queue()
        
        
    "Utility methods"
    def isAvalible(self):
        return self.stock > 0
    
    def updateStock(self, amount):
        self.stock += amount
        
    def toDict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "weight": self.weight,
            "value": self.value,
            "stock": self.stock,
            "reservation": self.reservations.toList()
        }
        
    def __str__(self):
        return f"[{self.isbn}] {self.title} - {self.author} | {self.weight} | {self.value} | {self.stock} | {self.reservations}"
