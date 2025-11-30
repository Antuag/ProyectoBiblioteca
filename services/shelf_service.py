from models.shelf import Shelf
from models.book import Book
from pathlib import Path
import json

# Ruta segura (independiente del lugar donde se ejecute el programa)
ruta = Path(__file__).resolve().parent.parent / "data" / "shelves.json"


def _load_shelves():
    """Función auxiliar para cargar los estantes desde el archivo JSON"""
    if ruta.is_file():
        try:
            with open(ruta, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def _save_shelves(shelves_list):
    """Función auxiliar para guardar los estantes en el archivo JSON"""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as file:
        json.dump(shelves_list, file, indent=4, ensure_ascii=False)


def _shelf_to_dict(shelf: Shelf):
    """Convierte un objeto Shelf a diccionario"""
    return {
        "id_shelf": shelf.id_shelf,
        "capacity": shelf.capacity,
        "books": [
            [
                {
                    "isbn": book.isbn,
                    "title": book.title,
                    "author": book.author,
                    "weight": book.weight,  # Mantener el nombre original de book.py
                    "value": book.value,
                    "stock": book.stock
                } if book is not None else None
                for book in row
            ]
            for row in shelf.books
        ]
    }


def create_shelf(shelf_data: Shelf):
    """
    Crea un nuevo estante en el archivo JSON.
    Si ya existe un estante con el mismo id_shelf, no lo crea y retorna None.
    """
    shelves_list = _load_shelves()
    
    # Verificar si ya existe un estante con ese ID
    for shelf in shelves_list:
        if shelf["id_shelf"] == shelf_data.id_shelf:
            print(f"Ya existe un estante con el ID: {shelf_data.id_shelf}")
            return None
    
    # Convertir el Shelf a diccionario y agregarlo
    shelf_dict = _shelf_to_dict(shelf_data)
    shelves_list.append(shelf_dict)
    
    # Guardar archivo
    _save_shelves(shelves_list)
    
    return shelf_data


def update_shelf(shelf_data: Shelf):
    """
    Actualiza un estante existente en el archivo JSON.
    Si no existe, retorna None.
    """
    shelves_list = _load_shelves()
    
    # Buscar y actualizar el estante
    for i, shelf in enumerate(shelves_list):
        if shelf["id_shelf"] == shelf_data.id_shelf:
            shelves_list[i] = _shelf_to_dict(shelf_data)
            _save_shelves(shelves_list)
            return shelf_data
    
    print(f"No se encontró un estante con el ID: {shelf_data.id_shelf}")
    return None


def create_or_update_shelf(shelf_data: Shelf):
    """
    Crea un nuevo estante o actualiza uno existente.
    """
    shelves_list = _load_shelves()
    
    # Buscar si ya existe
    for i, shelf in enumerate(shelves_list):
        if shelf["id_shelf"] == shelf_data.id_shelf:
            # Actualizar
            shelves_list[i] = _shelf_to_dict(shelf_data)
            _save_shelves(shelves_list)
            return shelf_data
    
    # Si no existe, crear
    shelf_dict = _shelf_to_dict(shelf_data)
    shelves_list.append(shelf_dict)
    _save_shelves(shelves_list)
    
    return shelf_data


def get_shelves():
    """
    Obtiene todos los estantes desde el archivo JSON.
    """
    shelves_list = _load_shelves()
    shelves = []
    
    for shelf_dict in shelves_list:
        shelf = Shelf(shelf_dict["id_shelf"])
        
        # Reconstruir la matriz de libros
        for i in range(5):
            for j in range(4):
                book_data = shelf_dict["books"][i][j]
                if book_data is not None:
                    book = Book(
                        isbn=book_data["isbn"],
                        title=book_data["title"],
                        author=book_data["author"],
                        weight=book_data["weight"],
                        value=book_data.get("value", 0),  # Valor por defecto si no existe
                        stock=book_data.get("stock", 1)   # Valor por defecto si no existe
                    )
                    shelf.books[i][j] = book
        
        shelves.append(shelf)
    
    return shelves


def get_shelf_by_id(id_shelf):
    """
    Obtiene un estante específico por su ID.
    """
    shelves_list = _load_shelves()
    
    for shelf_dict in shelves_list:
        if shelf_dict["id_shelf"] == id_shelf:
            shelf = Shelf(shelf_dict["id_shelf"])
            
            # Reconstruir la matriz de libros
            for i in range(5):
                for j in range(4):
                    book_data = shelf_dict["books"][i][j]
                    if book_data is not None:
                        book = Book(
                            isbn=book_data["isbn"],
                            title=book_data["title"],
                            author=book_data["author"],
                            weight=book_data["weight"],
                            value=book_data.get("value", 0),
                            stock=book_data.get("stock", 1)
                        )
                        shelf.books[i][j] = book
            
            return shelf
    
    return None


def delete_shelf(id_shelf):
    """
    Elimina un estante del archivo JSON.
    """
    shelves_list = _load_shelves()
    
    # Filtrar para eliminar el estante con ese ID
    new_shelves_list = [s for s in shelves_list if s["id_shelf"] != id_shelf]
    
    if len(new_shelves_list) == len(shelves_list):
        print(f"No se encontró un estante con el ID: {id_shelf}")
        return False
    
    _save_shelves(new_shelves_list)
    return True