class Book:
    # Definir siempre el ISBN con una estructura de 4 digitos para que cada digito sea un prefijo
    def __init__(self, isbn, title, author, weight, price):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.weight = weight
        self.price = price

