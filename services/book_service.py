from models.book import Book
from pathlib import Path
import json

# Ruta segura (independiente del lugar donde ejecutes el programa)
ruta = Path(__file__).resolve().parent.parent / "data" / "books.json"


def _load_books():
    """Función auxiliar para cargar los libros desde el archivo JSON"""
    if ruta.is_file():
        try:
            with open(ruta, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def _save_books(books_list):
    """Función auxiliar para guardar los libros en el archivo JSON"""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as file:
        json.dump(books_list, file, indent=4, ensure_ascii=False)


def _book_to_dict(book: Book):
    """Convierte un objeto Book a diccionario"""
    return {
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "weight": book.weight,
        "value": book.value,
        "stock": book.stock,
        "reservations": book.reservations.toList()
    }


def _dict_to_book(book_dict):
    """Convierte un diccionario a objeto Book"""
    book = Book(
        isbn=book_dict["isbn"],
        title=book_dict["title"],
        author=book_dict["author"],
        weight=book_dict["weight"],
        value=book_dict["value"],
        stock=book_dict.get("stock", 1)
    )
    
    # Reconstruir reservaciones si existen
    if "reservations" in book_dict and book_dict["reservations"]:
        from structures.queue import Queue
        for reservation in book_dict["reservations"]:
            book.reservations.enqueue(reservation)
    
    return book


def create_book(book: Book):
    """
    Crea un nuevo libro en el inventario.
    Si ya existe un libro con el mismo ISBN, no lo crea y retorna None.
    """
    if not isinstance(book, Book):
        raise TypeError("Debe ser un objeto de tipo Book")
    
    books_list = _load_books()
    
    # Verificar si ya existe un libro con ese ISBN
    for existing_book in books_list:
        if existing_book["isbn"] == book.isbn:
            print(f"Ya existe un libro con el ISBN: {book.isbn}")
            return None
    
    # Convertir el Book a diccionario y agregarlo
    book_dict = _book_to_dict(book)
    books_list.append(book_dict)
    
    # Guardar archivo
    _save_books(books_list)
    
    return book


def update_book(book: Book):
    """
    Actualiza un libro existente en el inventario por su ISBN.
    Si no existe, retorna None.
    """
    if not isinstance(book, Book):
        raise TypeError("Debe ser un objeto de tipo Book")
    
    books_list = _load_books()
    
    # Buscar y actualizar el libro
    for i, existing_book in enumerate(books_list):
        if existing_book["isbn"] == book.isbn:
            books_list[i] = _book_to_dict(book)
            _save_books(books_list)
            return book
    
    print(f"No se encontró un libro con el ISBN: {book.isbn}")
    return None


def create_or_update_book(book: Book):
    """
    Crea un nuevo libro o actualiza uno existente.
    """
    if not isinstance(book, Book):
        raise TypeError("Debe ser un objeto de tipo Book")
    
    books_list = _load_books()
    
    # Buscar si ya existe
    for i, existing_book in enumerate(books_list):
        if existing_book["isbn"] == book.isbn:
            # Actualizar
            books_list[i] = _book_to_dict(book)
            _save_books(books_list)
            return book
    
    # Si no existe, crear
    book_dict = _book_to_dict(book)
    books_list.append(book_dict)
    _save_books(books_list)
    
    return book


def get_all_books():
    """
    Obtiene todos los libros del inventario.
    Retorna una lista de objetos Book.
    """
    books_list = _load_books()
    return [_dict_to_book(book_dict) for book_dict in books_list]


def get_book_by_isbn(isbn):
    """
    Obtiene un libro específico por su ISBN.
    Retorna un objeto Book o None si no existe.
    """
    books_list = _load_books()
    
    for book_dict in books_list:
        if book_dict["isbn"] == str(isbn):
            return _dict_to_book(book_dict)
    
    return None


def delete_book(isbn):
    """
    Elimina un libro del inventario por su ISBN.
    Retorna True si se eliminó, False si no se encontró.
    """
    books_list = _load_books()
    
    # Filtrar para eliminar el libro con ese ISBN
    new_books_list = [book for book in books_list if book["isbn"] != str(isbn)]
    
    if len(new_books_list) == len(books_list):
        print(f"No se encontró un libro con el ISBN: {isbn}")
        return False
    
    _save_books(new_books_list)
    return True


def search_books_by_title(title):
    """
    Busca libros por título (búsqueda parcial, no case-sensitive).
    Retorna una lista de objetos Book que coinciden.
    """
    books_list = _load_books()
    matching_books = []
    
    title_lower = title.lower()
    for book_dict in books_list:
        if title_lower in book_dict["title"].lower():
            matching_books.append(_dict_to_book(book_dict))
    
    return matching_books


def search_books_by_author(author):
    """
    Busca libros por autor (búsqueda parcial, no case-sensitive).
    Retorna una lista de objetos Book que coinciden.
    """
    books_list = _load_books()
    matching_books = []
    
    author_lower = author.lower()
    for book_dict in books_list:
        if author_lower in book_dict["author"].lower():
            matching_books.append(_dict_to_book(book_dict))
    
    return matching_books


def get_available_books():
    """
    Obtiene todos los libros que tienen stock disponible.
    Retorna una lista de objetos Book con stock > 0.
    """
    books_list = _load_books()
    available_books = []
    
    for book_dict in books_list:
        if book_dict.get("stock", 0) > 0:
            available_books.append(_dict_to_book(book_dict))
    
    return available_books


def update_stock(isbn, amount):
    """
    Actualiza el stock de un libro.
    amount puede ser positivo (aumentar) o negativo (disminuir).
    Retorna el libro actualizado o None si no existe.
    """
    book = get_book_by_isbn(isbn)
    
    if book is None:
        print(f"No se encontró un libro con el ISBN: {isbn}")
        return None
    
    book.updateStock(amount)
    
    # Si el stock es negativo, ajustarlo a 0
    if book.stock < 0:
        book.stock = 0
    
    return update_book(book)


def get_inventory_stats():
    """
    Obtiene estadísticas del inventario.
    Retorna un diccionario con información resumida.
    """
    books_list = _load_books()
    
    total_books = len(books_list)
    total_stock = sum(book.get("stock", 0) for book in books_list)
    available_books = sum(1 for book in books_list if book.get("stock", 0) > 0)
    out_of_stock = total_books - available_books
    total_value = sum(book.get("value", 0) * book.get("stock", 0) for book in books_list)
    
    return {
        "total_books": total_books,
        "total_stock": total_stock,
        "available_books": available_books,
        "out_of_stock": out_of_stock,
        "total_inventory_value": total_value
    }


def get_low_stock_books(threshold=5):
    """
    Obtiene libros con stock bajo (por defecto <= 5 unidades).
    Retorna una lista de objetos Book.
    """
    books_list = _load_books()
    low_stock_books = []
    
    for book_dict in books_list:
        if 0 < book_dict.get("stock", 0) <= threshold:
            low_stock_books.append(_dict_to_book(book_dict))
    
    return low_stock_books