from book import Book
class Shelf:
    def __init__(self, id_shelf):
        self.id_shelf = id_shelf
        self.capacity = (
            20  # Su capacidad es fija ya que cada estante tiene 4 filas 5 columnas
        )
        self.books = [
            [None for _ in range(4)] for _ in range(5)
        ]  # Matriz 4x5 para almacenar books

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Debe ser un objeto de tipo Book")
        for i in range(5):
            shelf_weight = sum(
                b.weight for b in self.books[i] if b is not None
            )  # Peso total actual de la fila

            if shelf_weight + book.weight > 8:  # Peso total actual de la fila
                continue
            for j in range(4):  # Buscar espacio vacío
                if self.books[i][j] is None:
                    self.books[i][j] = book
                    return True
        return False

    def remove_book(self, isbn):
        for i in range(5):
            for j in range(4):
                if (
                    self.books[i][j] is not None and self.books[i][j].isbn == isbn
                ):  # Encontrar el libro por ISBN
                    self.books[i][j] = None
                    return True
        return False

    def find_book(self, isbn):
        for i in range(5):
            for j in range(4):
                if (
                    self.books[i][j] is not None and self.books[i][j].isbn == isbn
                ):  # Encontrar el libro por ISBN
                    return (i, j) # Retornar la posición (fila, columna) ojoooo hay que desempaquetar la tupla al usarla
        return None


    def replace_book(self, isbn, new_book: Book):
        if not isinstance(new_book, Book):
            raise TypeError("Debe ser un objeto de tipo Book")

        position = self.find_book(isbn)

        if position is not None:
            i, j = position
            # Peso del estante si quitáramos el libro viejo
            shelf_weight = (
                sum(b.weight for b in self.books[i] if b is not None)
                - self.books[i][j].weight
            )
            # Verificar que el nuevo libro no exceda el límite
            if shelf_weight + new_book.weight <= 8:
                self.books[i][j] = new_book
                return True
        return False # No se encontró el libro o no se pudo reemplazar
