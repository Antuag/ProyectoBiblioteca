from models.book import Book

class Shelf:
    # Constantes para mayor claridad y mantenibilidad
    ROWS = 5  # Número de estantes horizontales
    COLUMNS = 4  # Número de espacios por estante
    MAX_WEIGHT_PER_ROW = 8  # Peso máximo en kg por estante
    CAPACITY = ROWS * COLUMNS  # 20 libros en total
    
    def __init__(self, id_shelf):
        self.id_shelf = id_shelf
        self.capacity = self.CAPACITY
        # Matriz: 5 filas (estantes) x 4 columnas (espacios)
        self.books = [
            [None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)
        ]

    def get_row_weight(self, row_index):
        """Calcula el peso total de una fila específica"""
        return sum(book.weight for book in self.books[row_index] if book is not None)

    def get_available_spaces(self):
        """Retorna el número de espacios vacíos en el estante"""
        count = 0
        for row in self.books:
            count += sum(1 for space in row if space is None)
        return count

    def is_full(self):
        """Verifica si el estante está completamente lleno"""
        return self.get_available_spaces() == 0

    def add_book(self, book: Book):
        """
        Agrega un libro al estante.
        Busca la primera fila que pueda soportar su peso.
        Retorna True si se agregó exitosamente, False en caso contrario.
        """
        if not isinstance(book, Book):
            raise TypeError("Debe ser un objeto de tipo Book")
        
        # Iterar por cada fila (estante horizontal)
        for i in range(self.ROWS):
            row_weight = self.get_row_weight(i)
            
            # Verificar si agregar el libro excedería el peso máximo de la fila
            if row_weight + book.weight > self.MAX_WEIGHT_PER_ROW:
                continue  # Esta fila no puede soportar el libro
            
            # Buscar espacio vacío en la fila
            for j in range(self.COLUMNS):
                if self.books[i][j] is None:
                    self.books[i][j] = book
                    return True
        
        # No se encontró espacio disponible
        return False

    def remove_book(self, isbn):
        """
        Remueve un libro del estante por su ISBN.
        Retorna True si se removió exitosamente, False si no se encontró.
        """
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if self.books[i][j] is not None and self.books[i][j].isbn == isbn:
                    self.books[i][j] = None
                    return True
        return False

    def find_book(self, isbn):
        """
        Busca un libro por ISBN.
        Retorna una tupla (fila, columna) si lo encuentra, None en caso contrario.
        """
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if self.books[i][j] is not None and self.books[i][j].isbn == isbn:
                    return (i, j)
        return None

    def replace_book(self, isbn, new_book: Book):
        """
        Reemplaza un libro existente con uno nuevo.
        Verifica que el nuevo libro no exceda el límite de peso de la fila.
        Retorna True si se reemplazó exitosamente, False en caso contrario.
        """
        if not isinstance(new_book, Book):
            raise TypeError("Debe ser un objeto de tipo Book")

        position = self.find_book(isbn)

        if position is not None:
            i, j = position
            old_book = self.books[i][j]
            
            # Calcular peso de la fila sin el libro viejo + con el libro nuevo
            row_weight_without_old = self.get_row_weight(i) - old_book.weight
            
            # Verificar que el nuevo libro no exceda el límite
            if row_weight_without_old + new_book.weight <= self.MAX_WEIGHT_PER_ROW:
                self.books[i][j] = new_book
                return True
        
        return False  # No se encontró el libro o no se pudo reemplazar

    def get_books_list(self):
        """Retorna una lista plana con todos los libros del estante (sin None)"""
        books_list = []
        for row in self.books:
            for book in row:
                if book is not None:
                    books_list.append(book)
        return books_list

    def get_shelf_info(self):
        """Retorna información resumida del estante"""
        total_books = self.CAPACITY - self.get_available_spaces()
        total_weight = sum(
            book.weight for row in self.books for book in row if book is not None
        )
        
        return {
            "id_shelf": self.id_shelf,
            "capacity": self.CAPACITY,
            "total_books": total_books,
            "available_spaces": self.get_available_spaces(),
            "total_weight": round(total_weight, 2),
            "is_full": self.is_full()
        }

    def __str__(self):
        """Representación en string del estante"""
        info = self.get_shelf_info()
        return (f"Shelf {self.id_shelf}: {info['total_books']}/{self.CAPACITY} libros | "
                f"Peso total: {info['total_weight']}kg | "
                f"Espacios disponibles: {info['available_spaces']}")

    def display_shelf(self):
        """Muestra el estante de forma visual"""
        print(f"\n{'='*60}")
        print(f"ESTANTE #{self.id_shelf}")
        print(f"{'='*60}")
        
        for i in range(self.ROWS):
            row_weight = self.get_row_weight(i)
            print(f"\nFila {i} (Peso: {row_weight:.2f}/{self.MAX_WEIGHT_PER_ROW}kg):")
            
            for j in range(self.COLUMNS):
                book = self.books[i][j]
                if book is not None:
                    print(f"  [{j}] {book.title[:30]} - {book.weight}kg")
                else:
                    print(f"  [{j}] [Vacío]")
        
        print(f"\n{'='*60}")
        print(self)
        print(f"{'='*60}\n")
