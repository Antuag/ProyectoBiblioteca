from models.book import Book
from pathlib import Path
from algorithms.insertion_sort import insertion_sort_books_by_isbn
import json

# ==============================================================
# RUTAS: Inventario General (desordenado) & Inventario Ordenado
# ==============================================================

ruta_general = Path(__file__).resolve().parent.parent / "data" / "books.json"
ruta_ordenado = Path(__file__).resolve().parent.parent / "data" / "sorted_books.json"

# ==============================================================
# FUNCIONES INTERNAS DE ARCHIVO
# ==============================================================

def _load_json(path):
    """Carga un JSON desde la ruta dada."""
    if path.is_file():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def _save_json(path, data):
    """Guarda un JSON en la ruta dada."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ==============================================================
# CONVERSIÓN OBJETO <--> DICCIONARIO
# ==============================================================

def _book_to_dict(book: Book):
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
    book = Book(
        isbn=book_dict["isbn"],
        title=book_dict["title"],
        author=book_dict["author"],
        weight=book_dict["weight"],
        value=book_dict["value"],
        stock=book_dict.get("stock", 1)
    )

    # Reconstruir reservaciones si existen
    if "reservations" in book_dict:
        for r in book_dict["reservations"]:
            # Normalizar: aceptar tanto string como dict
            if isinstance(r, str):
                reservation = {
                    "user_id": r,
                    "date": "unknown"
                }
            else:
                reservation = r
            book.reservations.enqueue(reservation)

    return book


# ==============================================================
# CREAR LIBRO (DOS LISTAS)
# ==============================================================

def create_book(book: Book):
    """Crea un libro en el inventario general y en el inventario ordenado."""
    if not isinstance(book, Book):
        raise TypeError("Debe ser un objeto Book")

    general = _load_json(ruta_general)
    ordenado = _load_json(ruta_ordenado)

    # Evitar duplicados
    for b in general:
        if b["isbn"] == book.isbn:
            print(f"❌ Ya existe un libro con ISBN {book.isbn}")
            return None

    book_dict = _book_to_dict(book)

    # 1. Inventario general = append directo
    general.append(book_dict)
    _save_json(ruta_general, general)

    # 2. Inventario ordenado = append + insertion sort
    ordenado.append(book_dict)
    insertion_sort_books_by_isbn(ordenado)
    _save_json(ruta_ordenado, ordenado)

    return book


# ==============================================================
# LECTURA (DOS LISTAS)
# ==============================================================

def get_all_books():
    """Retorna el inventario GENERAL (desordenado)."""
    lista = _load_json(ruta_general)
    return [_dict_to_book(b) for b in lista]


def get_ordered_books():
    lista = _load_json(ruta_ordenado)

    # Si el archivo no existe o está vacío → reconstruirlo desde books.json
    if not lista:
        general = _load_json(ruta_general)
        insertion_sort_books_by_isbn(general)
        _save_json(ruta_ordenado, general)
        lista = general

    return [_dict_to_book(b) for b in lista]



# ==============================================================
# BÚSQUEDA POR ISBN (BINARIA SOBRE LISTA ORDENADA)
# ==============================================================

def get_book_by_isbn(isbn):
    from algorithms.binary_search import binary_search_isbn
    ordered_books = get_ordered_books()
    return binary_search_isbn(ordered_books, isbn)


# ==============================================================
# UPDATE (ACTUALIZAR DATOS)
# ==============================================================

def update_book(book: Book):
    """Actualiza un libro en ambas listas JSON."""

    if not isinstance(book, Book):
        raise TypeError("Debe ser un objeto Book")

    # Actualizar INVENTARIO GENERAL
    general = _load_json(ruta_general)
    updated = False

    for i, b in enumerate(general):
        if b["isbn"] == book.isbn:
            general[i] = _book_to_dict(book)
            updated = True
            break

    if not updated:
        print(f"❌ No se encontró un libro con ISBN {book.isbn}")
        return None

    _save_json(ruta_general, general)

    # Actualizar INVENTARIO ORDENADO
    ordenado = _load_json(ruta_ordenado)

    # Si no existe el archivo ordenado, lo regeneramos completo
    if not ordenado:
        ordenado = general.copy()

    for i, b in enumerate(ordenado):
        if b["isbn"] == book.isbn:
            ordenado[i] = _book_to_dict(book)
            break

    # Reordenar con insertion sort
    insertion_sort_books_by_isbn(ordenado)
    _save_json(ruta_ordenado, ordenado)

    return book




# ==============================================================
# DELETE
# ==============================================================

def delete_book(isbn):
    """Elimina un libro en ambas listas JSON."""

    # GENERAL
    general = _load_json(ruta_general)
    new_general = [b for b in general if b["isbn"] != str(isbn)]

    if len(new_general) == len(general):
        print(f"❌ No existe un libro con ISBN {isbn}")
        return False

    _save_json(ruta_general, new_general)

    # ORDENADO
    ordenado = _load_json(ruta_ordenado)
    if ordenado:
        new_ord = [b for b in ordenado if b["isbn"] != str(isbn)]
        _save_json(ruta_ordenado, new_ord)

    return True


# ==============================================================
# BÚSQUEDA LINEAL (TÍTULO / AUTOR)
# ==============================================================

def search_books_by_title(title):
    general = _load_json(ruta_general)
    title = title.lower()
    return [_dict_to_book(b) for b in general if title in b["title"].lower()]


def search_books_by_author(author):
    general = _load_json(ruta_general)
    author = author.lower()
    return [_dict_to_book(b) for b in general if author in b["author"].lower()]


# ==============================================================
# LIBROS DISPONIBLES / STOCK BAJO
# ==============================================================

def get_available_books():
    general = _load_json(ruta_general)
    return [_dict_to_book(b) for b in general if b.get("stock", 0) > 0]


def get_low_stock_books(threshold=5):
    general = _load_json(ruta_general)
    return [_dict_to_book(b) for b in general if 0 < b.get("stock", 0) <= threshold]


# ==============================================================
# UPDATE STOCK
# ==============================================================

def update_stock(isbn, amount):
    book = get_book_by_isbn(isbn)
    if not book:
        print(f"No existe libro con ISBN {isbn}")
        return None

    book.updateStock(amount)

    if book.stock < 0:
        book.stock = 0

    return update_book(book)


# ==============================================================
# ESTADÍSTICAS
# ==============================================================

def get_inventory_stats():
    general = _load_json(ruta_general)

    total_books = len(general)
    total_stock = sum(b.get("stock", 0) for b in general)
    available_books = sum(1 for b in general if b.get("stock", 0) > 0)
    out_of_stock = total_books - available_books
    total_value = sum(b.get("value", 0) * b.get("stock", 0) for b in general)

    return {
        "total_books": total_books,
        "total_stock": total_stock,
        "available_books": available_books,
        "out_of_stock": out_of_stock,
        "total_inventory_value": total_value
    }
# ==============================================================
# RESERVATIONS QUEUE HELPERS
# ==============================================================

def dequeue_reservation(isbn):
    """
    Dequeue the next reservation (FIFO) for a given book.
    It uses binary search on the ordered inventory to locate the book.

    Args:
        isbn (str): Book ISBN

    Returns:
        dict | None: reservation {"user_id": ..., "date": ...} or None if empty
    """
    book = get_book_by_isbn(isbn)  # binary search over ordered list
    if not book:
        print(f"❌ Book with ISBN {isbn} not found while checking reservations.")
        return None

    if book.reservations.is_empty():
        return None

    next_reservation = book.reservations.dequeue()
    update_book(book)
    return next_reservation


def has_reservations(isbn):
    """
    Check if a book has pending reservations.

    Args:
        isbn (str): Book ISBN

    Returns:
        bool
    """
    book = get_book_by_isbn(isbn)
    return bool(book and not book.reservations.is_empty())
