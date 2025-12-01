import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.shelf_service import (
    create_shelf as service_create_shelf,
    update_shelf as service_update_shelf,
    create_or_update_shelf as service_create_or_update_shelf,
    get_shelves as service_get_shelves,
    get_shelf_by_id as service_get_shelf_by_id,
    delete_shelf as service_delete_shelf
)
from services.book_service import get_book_by_isbn as service_get_book_by_isbn
from models.shelf import Shelf
from models.book import Book
from algorithms.brute_force_shelf import brute_force_shelf_manual
from services.book_service import get_all_books

# Combinaciones válidas generadas con fuerza bruta
VALID_COMBINATIONS = []


def clear_screen():
    """Limpia la consola"""
    print("\n" * 2)


def pause():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresiona Enter para continuar...")


def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_shelf_summary(shelf: Shelf, index=None):
    """Imprime un resumen del estante"""
    prefix = f"[{index + 1}]" if index is not None else "→"
    info = shelf.get_shelf_info()
    
    print(f"\n{prefix} ID Estante: {shelf.id_shelf}")
    print(f"   Capacidad: {info['capacity']} libros")
    print(f"   Libros actuales: {info['total_books']}")
    print(f"   Espacios disponibles: {info['available_spaces']}")
    print(f"   Peso total: {info['total_weight']} kg")
    print(f"   Estado: {'Lleno' if info['is_full'] else 'Disponible'}")


def print_shelf_detail(shelf: Shelf):
    """Imprime el detalle completo del estante"""
    print_header(f"ESTANTE #{shelf.id_shelf}")
    
    for i in range(shelf.ROWS):
        row_weight = shelf.get_row_weight(i)
        print(f"\nFila {i + 1} (Peso: {row_weight:.2f}/{shelf.MAX_WEIGHT_PER_ROW} kg):")
        
        for j in range(shelf.COLUMNS):
            book = shelf.books[i][j]
            if book is not None:
                print(f"  [{j + 1}] {book.title[:35]:35} | {book.weight:.2f}kg | ISBN: {book.isbn}")
            else:
                print(f"  [{j + 1}] [Vacío]")
    
    info = shelf.get_shelf_info()
    print(f"\n{'='*60}")
    print(f"Total: {info['total_books']}/{info['capacity']} libros | Peso: {info['total_weight']}kg")
    print(f"{'='*60}")


def create_shelf():
    """Opción 1: Crear un nuevo estante"""
    print_header("CREAR NUEVO ESTANTE")
    
    id_shelf = input("\nIngrese ID del estante: ").strip()
    if not id_shelf:
        print("❌ El ID no puede estar vacío")
        return
    
    # Verificar si ya existe
    existing_shelf = service_get_shelf_by_id(id_shelf)
    if existing_shelf:
        print(f"❌ Ya existe un estante con el ID: {id_shelf}")
        return
    
    # Crear el estante
    new_shelf = Shelf(id_shelf)
    result = service_create_shelf(new_shelf)
    
    if result:
        print("\n✅ Estante creado exitosamente")
        print_shelf_summary(new_shelf)
    else:
        print("\n❌ No se pudo crear el estante")


def list_all_shelves():
    """Opción 2: Listar todos los estantes"""
    print_header("TODOS LOS ESTANTES")
    
    shelves = service_get_shelves()
    
    if not shelves:
        print("\n📦 No hay estantes registrados")
        return
    
    print(f"\nTotal de estantes: {len(shelves)}")
    
    for i, shelf in enumerate(shelves):
        print_shelf_summary(shelf, i)


def view_shelf_detail():
    """Opción 3: Ver detalle de un estante"""
    print_header("DETALLE DE ESTANTE")
    
    id_shelf = input("\nIngrese ID del estante: ").strip()
    shelf = service_get_shelf_by_id(id_shelf)
    
    if not shelf:
        print(f"\n❌ No se encontró un estante con el ID: {id_shelf}")
        return
    
    print_shelf_detail(shelf)


def add_book_to_shelf():
    """Opción 4: Agregar libro a un estante"""
    print_header("AGREGAR LIBRO A ESTANTE")
    
    id_shelf = input("\nIngrese ID del estante: ").strip()
    shelf = service_get_shelf_by_id(id_shelf)
    
    if not shelf:
        print(f"\n❌ No se encontró un estante con el ID: {id_shelf}")
        return
    
    print("\n📚 Estante seleccionado:")
    print_shelf_summary(shelf)
    
    if shelf.is_full():
        print("\n⚠️ El estante está lleno. No se pueden agregar más libros.")
        return
    
    isbn = input("\nIngrese ISBN del libro a agregar: ").strip()
    book = service_get_book_by_isbn(isbn)
    
    if not book:
        print(f"\n❌ No se encontró un libro con el ISBN: {isbn}")
        return
    
    print(f"\n📖 Libro: {book.title}")
    print(f"   Autor: {book.author}")
    print(f"   Peso: {book.weight} kg")
    
    # Intentar agregar el libro
    success = shelf.add_book(book)
    
    if success:
        # Guardar el estante actualizado
        result = service_update_shelf(shelf)
        if result:
            print("\n✅ Libro agregado exitosamente al estante")
            print_shelf_summary(shelf)
        else:
            print("\n❌ Error al guardar el estante")
    else:
        print("\n❌ No se pudo agregar el libro al estante")
        print("   Razones posibles:")
        print("   - Ninguna fila tiene espacio disponible")
        print("   - El peso del libro excede el límite de todas las filas")


def remove_book_from_shelf():
    """Opción 5: Remover libro de un estante"""
    print_header("REMOVER LIBRO DE ESTANTE")
    
    id_shelf = input("\nIngrese ID del estante: ").strip()
    shelf = service_get_shelf_by_id(id_shelf)
    
    if not shelf:
        print(f"\n❌ No se encontró un estante con el ID: {id_shelf}")
        return
    
    print("\n📚 Estante seleccionado:")
    print_shelf_detail(shelf)
    
    isbn = input("\nIngrese ISBN del libro a remover: ").strip()
    
    # Buscar el libro en el estante
    position = shelf.find_book(isbn)
    
    if not position:
        print(f"\n❌ El libro con ISBN {isbn} no está en este estante")
        return
    
    i, j = position
    book = shelf.books[i][j]
    
    print(f"\n📖 Libro encontrado:")
    print(f"   Título: {book.title}")
    print(f"   Posición: Fila {i + 1}, Columna {j + 1}")
    
    confirm = input("\n⚠️  ¿Está seguro de remover este libro del estante? (s/n): ").strip().lower()
    
    if confirm == "s":
        success = shelf.remove_book(isbn)
        if success:
            result = service_update_shelf(shelf)
            if result:
                print("\n✅ Libro removido exitosamente del estante")
                print_shelf_summary(shelf)
            else:
                print("\n❌ Error al guardar el estante")
        else:
            print("\n❌ No se pudo remover el libro")
    else:
        print("\n❌ Operación cancelada")


def replace_book_in_shelf():
    """Opción 6: Reemplazar un libro en el estante"""
    print_header("REEMPLAZAR LIBRO EN ESTANTE")
    
    id_shelf = input("\nIngrese ID del estante: ").strip()
    shelf = service_get_shelf_by_id(id_shelf)
    
    if not shelf:
        print(f"\n❌ No se encontró un estante con el ID: {id_shelf}")
        return
    
    print("\n📚 Estante seleccionado:")
    print_shelf_detail(shelf)
    
    old_isbn = input("\nIngrese ISBN del libro a reemplazar: ").strip()
    
    # Buscar el libro viejo
    position = shelf.find_book(old_isbn)
    
    if not position:
        print(f"\n❌ El libro con ISBN {old_isbn} no está en este estante")
        return
    
    i, j = position
    old_book = shelf.books[i][j]
    
    print(f"\n📖 Libro actual:")
    print(f"   Título: {old_book.title}")
    print(f"   Peso: {old_book.weight} kg")
    print(f"   Posición: Fila {i + 1}, Columna {j + 1}")
    
    new_isbn = input("\nIngrese ISBN del nuevo libro: ").strip()
    new_book = service_get_book_by_isbn(new_isbn)
    
    if not new_book:
        print(f"\n❌ No se encontró un libro con el ISBN: {new_isbn}")
        return
    
    print(f"\n📖 Nuevo libro:")
    print(f"   Título: {new_book.title}")
    print(f"   Peso: {new_book.weight} kg")
    
    # Verificar si el reemplazo es posible
    row_weight = shelf.get_row_weight(i) - old_book.weight
    if row_weight + new_book.weight > shelf.MAX_WEIGHT_PER_ROW:
        print(f"\n❌ El nuevo libro es demasiado pesado para esta fila")
        print(f"   Peso actual de la fila sin el libro viejo: {row_weight:.2f} kg")
        print(f"   Peso del nuevo libro: {new_book.weight} kg")
        print(f"   Total: {row_weight + new_book.weight:.2f} kg (máximo: {shelf.MAX_WEIGHT_PER_ROW} kg)")
        return
    
    success = shelf.replace_book(old_isbn, new_book)
    
    if success:
        result = service_update_shelf(shelf)
        if result:
            print("\n✅ Libro reemplazado exitosamente")
            print_shelf_summary(shelf)
        else:
            print("\n❌ Error al guardar el estante")
    else:
        print("\n❌ No se pudo reemplazar el libro")


def search_book_in_shelves():
    """Opción 7: Buscar en qué estante está un libro"""
    print_header("BUSCAR LIBRO EN ESTANTES")
    
    isbn = input("\nIngrese ISBN del libro a buscar: ").strip()
    
    # Buscar el libro en el inventario primero
    book = service_get_book_by_isbn(isbn)
    if book:
        print(f"\n📖 Libro: {book.title}")
        print(f"   Autor: {book.author}")
        print(f"   Peso: {book.weight} kg")
    
    # Buscar en todos los estantes
    shelves = service_get_shelves()
    found_in = []
    
    for shelf in shelves:
        position = shelf.find_book(isbn)
        if position:
            i, j = position
            found_in.append({
                'shelf': shelf,
                'row': i,
                'col': j
            })
    
    if not found_in:
        print(f"\n❌ El libro con ISBN {isbn} no está en ningún estante")
        return
    
    print(f"\n✅ Libro encontrado en {len(found_in)} estante(s):")
    
    for item in found_in:
        shelf = item['shelf']
        print(f"\n→ Estante: {shelf.id_shelf}")
        print(f"   Posición: Fila {item['row'] + 1}, Columna {item['col'] + 1}")
        print(f"   Ocupación: {shelf.get_shelf_info()['total_books']}/{shelf.capacity} libros")


def delete_shelf():
    """Opción 8: Eliminar un estante"""
    print_header("ELIMINAR ESTANTE")
    
    id_shelf = input("\nIngrese ID del estante a eliminar: ").strip()
    shelf = service_get_shelf_by_id(id_shelf)
    
    if not shelf:
        print(f"\n❌ No se encontró un estante con el ID: {id_shelf}")
        return
    
    print("\n📚 Estante a eliminar:")
    print_shelf_summary(shelf)
    
    # Verificar si tiene libros
    info = shelf.get_shelf_info()
    if info['total_books'] > 0:
        print(f"\n⚠️  ADVERTENCIA: Este estante tiene {info['total_books']} libro(s)")
        print("   Al eliminarlo, los libros quedarán sin ubicación física")
    
    confirm = input("\n⚠️  ¿Está seguro de eliminar este estante? (s/n): ").strip().lower()
    
    if confirm == "s":
        result = service_delete_shelf(id_shelf)
        if result:
            print("\n✅ Estante eliminado exitosamente")
        else:
            print("\n❌ No se pudo eliminar el estante")
    else:
        print("\n❌ Operación cancelada")


def view_shelf_statistics():
    """Opción 9: Ver estadísticas de los estantes"""
    print_header("ESTADÍSTICAS DE ESTANTES")
    
    shelves = service_get_shelves()
    
    if not shelves:
        print("\n📦 No hay estantes registrados")
        return
    
    total_shelves = len(shelves)
    total_capacity = sum(shelf.capacity for shelf in shelves)
    total_books = sum(shelf.get_shelf_info()['total_books'] for shelf in shelves)
    total_weight = sum(shelf.get_shelf_info()['total_weight'] for shelf in shelves)
    full_shelves = sum(1 for shelf in shelves if shelf.is_full())
    empty_shelves = sum(1 for shelf in shelves if shelf.get_shelf_info()['total_books'] == 0)
    
    print(f"\n📊 Resumen general:")
    print(f"\n   Total de estantes: {total_shelves}")
    print(f"   Capacidad total: {total_capacity} libros")
    print(f"   Libros colocados: {total_books}")
    print(f"   Espacios disponibles: {total_capacity - total_books}")
    print(f"   Ocupación: {(total_books/total_capacity*100):.1f}%")
    print(f"   Peso total: {total_weight:.2f} kg")
    print(f"   Estantes llenos: {full_shelves}")
    print(f"   Estantes vacíos: {empty_shelves}")


def generate_shelf_combinations():
    """Genera todas las combinaciones válidas de 4 libros (A5 Fuerza Bruta)."""
    global VALID_COMBINATIONS

    print_header("GENERAR COMBINACIONES (FUERZA BRUTA)")

    books = get_all_books()

    if len(books) < 4:
        print("\n❌ Se necesitan al menos 4 libros en el inventario.")
        return

    print("\n⏳ Generando combinaciones, por favor espere...")
    VALID_COMBINATIONS = brute_force_shelf_manual(books, max_weight=8)

    print(f"\n✅ Combinaciones generadas correctamente: {len(VALID_COMBINATIONS)} encontradas.")


def save_bruteforce_shelf():
    """Permite elegir una combinación válida y guardarla como estante."""
    if not VALID_COMBINATIONS:
        print("\n❌ Primero genere las combinaciones (opción 10).")
        return

    print_header("GUARDAR ESTANTE DESDE COMBINACIÓN")

    for idx, combo in enumerate(VALID_COMBINATIONS):
        titles = [b.title for b in combo]
        weight = sum(b.weight for b in combo)
        print(f"{idx + 1}. {titles} | Peso total: {weight:.2f} kg")

    try:
        choice = int(input("\nSeleccione número de combinación: ")) - 1
    except ValueError:
        print("\n❌ Opción inválida.")
        return

    if choice < 0 or choice >= len(VALID_COMBINATIONS):
        print("\n❌ El número no corresponde a una combinación válida.")
        return

    selected = VALID_COMBINATIONS[choice]

    shelf_id = input("\nIngrese ID para el nuevo estante: ").strip()

    if service_get_shelf_by_id(shelf_id):
        print("\n❌ Ya existe un estante con ese ID.")
        return

    # Crear estante
    shelf = Shelf(shelf_id)

    # Asignar los 4 libros a la primera fila
    for col in range(4):
        shelf.books[0][col] = selected[col]

    result = service_create_shelf(shelf)

    if result:
        print("\n✅ Estante creado exitosamente con la combinación seleccionada.")
    else:
        print("\n❌ No se pudo crear el estante.")


def show_menu():
    """Muestra el menú principal de estantes"""
    print_header("SISTEMA DE GESTIÓN DE ESTANTES")
    print("\n1. Crear nuevo estante")
    print("2. Listar todos los estantes")
    print("3. Ver detalle de un estante")
    print("4. Agregar libro a estante")
    print("5. Remover libro de estante")
    print("6. Reemplazar libro en estante")
    print("7. Buscar libro en estantes")
    print("8. Eliminar estante")
    print("9. Ver estadísticas de estantes")
    print("10. Generar combinaciones (A5 Fuerza Bruta)")
    print("11. Crear estante desde combinación válida")
    print("0. Salir")


def shelf_menu():
    """Función principal del menú de estantes"""
    while True:
        clear_screen()
        show_menu()
        
        option = input("\nSeleccione una opción: ").strip()
        
        if option == "1":
            create_shelf()
        elif option == "2":
            list_all_shelves()
        elif option == "3":
            view_shelf_detail()
        elif option == "4":
            add_book_to_shelf()
        elif option == "5":
            remove_book_from_shelf()
        elif option == "6":
            replace_book_in_shelf()
        elif option == "7":
            search_book_in_shelves()
        elif option == "8":
            delete_shelf()
        elif option == "9":
            view_shelf_statistics()
        elif option == "10":
            generate_shelf_combinations()
        elif option == "11":
            save_bruteforce_shelf()
        elif option == "0":
            print("\n👋 Regresando al menú principal...")
            break
        else:
            print("\n❌ Opción no válida. Por favor, seleccione una opción del menú.")
        
        pause()


if __name__ == "__main__":
    shelf_menu()