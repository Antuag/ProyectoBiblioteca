import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.book_service import (
    create_book as service_create_book,
    get_all_books as service_get_all_books,
    get_book_by_isbn as service_get_book_by_isbn,
    update_book as service_update_book,
    delete_book as service_delete_book,
    get_available_books as service_get_available_books,
    get_low_stock_books as service_get_low_stock_books,
    update_stock as service_update_stock,
    get_inventory_stats as service_get_inventory_stats,
    get_ordered_books as service_get_ordered_books

)
from models.book import Book
"algoritmo para busqueda lineal por titulo o autor o isbn en busqueda binaria, "
from algorithms.linear_search import linear_search_books
from algorithms.binary_search import binary_search_isbn 
from algorithms.merge_sort import merge_sort_books_by_isbn



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


def print_book(book: Book, index=None):
    """Imprime la información de un libro de forma formateada"""
    prefix = f"[{index + 1}]" if index is not None else "→"
    print(f"\n{prefix} ISBN: {book.isbn}")
    print(f"   Título: {book.title}")
    print(f"   Autor: {book.author}")
    print(f"   Peso: {book.weight} kg")
    print(f"   Valor: ${book.value:,}")
    print(f"   Stock: {book.stock} unidades")
    print(f"   Disponible: {'Sí' if book.isAvalible() else 'No'}")


def add_book():
    """Opción 1: Agregar un nuevo libro al inventario"""
    print_header("AGREGAR NUEVO LIBRO")
    
    try:
        isbn = input("\nIngrese ISBN: ").strip()
        if not isbn:
            print("❌ El ISBN no puede estar vacío")
            return
        
        # Verificar si ya existe
        existing_book = service_get_book_by_isbn(isbn)
        if existing_book:
            print(f"❌ Ya existe un libro con el ISBN: {isbn}")
            return
        
        title = input("Ingrese título: ").strip()
        if not title:
            print("❌ El título no puede estar vacío")
            return
        
        author = input("Ingrese autor: ").strip()
        if not author:
            print("❌ El autor no puede estar vacío")
            return
        
        weight_input = input("Ingrese peso (kg): ").strip()
        weight = float(weight_input) if weight_input else 0
        if weight <= 0:
            print("❌ El peso debe ser mayor a 0")
            return
        
        value_input = input("Ingrese valor ($): ").strip()
        value = int(value_input) if value_input else 0
        if value < 0:
            print("❌ El valor no puede ser negativo")
            return
        
        stock_input = input("Ingrese stock inicial: ").strip()
        stock = int(stock_input) if stock_input else 0
        if stock < 0:
            print("❌ El stock no puede ser negativo")
            return
        
        # Crear el libro (usando 'weight' correcto)
        new_book = Book(
            isbn=isbn,
            title=title,
            author=author,
            weight=weight,
            value=value,
            stock=stock
        )
        result = service_create_book(new_book)
        
        if result:
            print("\n✅ Libro agregado exitosamente al inventario")
            print_book(new_book)
        else:
            print("\n❌ No se pudo agregar el libro")
    
    except ValueError:
        print("\n❌ Error: Ingrese valores numéricos válidos para peso, valor y stock")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def list_all_books():
    """Opción 2: Listar todos los libros"""
    print_header("INVENTARIO COMPLETO")
    
    books = service_get_all_books()
    
    if not books:
        print("\n📦 El inventario está vacío")
        return
    
    print(f"\nTotal de libros: {len(books)}")
    
    for i, book in enumerate(books):
        print_book(book, i)

def list_books_sorted_by_isbn():
    """Lista los libros ordenados por ISBN usando Merge Sort."""
    print_header("INVENTARIO ORDENADO POR ISBN (MERGE SORT)")
    
    books = service_get_all_books()
    if not books:
        print("\n📦 El inventario está vacío")
        return

    sorted_books = merge_sort_books_by_isbn(books)

    print(f"\nTotal de libros: {len(sorted_books)}")
    for i, book in enumerate(sorted_books):
        print_book(book, i)
    

def search_book():
    """Opción 3: Buscar libro (usa algoritmo de búsqueda lineal y binaria)."""
    print_header("BUSCAR LIBRO")

    print("\n¿Cómo desea buscar?")
    print("1. Por ISBN (búsqueda binaria)")
    print("2. Por título (búsqueda lineal)")
    print("3. Por autor (búsqueda lineal)")

    option = input("\nSeleccione una opción: ").strip()

    # -------------------------------
    # 1. BUSCAR POR ISBN (BINARIA)
    # -------------------------------
    if option == "1":
        books = merge_sort_books_by_isbn(service_get_all_books())
        isbn = input("\nIngrese ISBN: ").strip()
        book = binary_search_isbn(books, isbn)

        if book:
            print("\n✅ Libro encontrado:")
            print_book(book)
        else:
            print(f"\n❌ No se encontró ningún libro con el ISBN: {isbn}")
        return

    # -------------------------------
    # OBTENER LISTA DE LIBROS
    # -------------------------------
    books = service_get_all_books()

    if not books:
        print("\n❌ No hay libros en el inventario.")
        return

    # -------------------------------
    # 2. BÚSQUEDA LINEAL POR TÍTULO
    # -------------------------------
    if option == "2":
        title = input("\nIngrese título (coincidencia parcial): ").strip()

        # tu algoritmo lineal aquí ⬇⬇⬇
        matches = linear_search_books(books, title=title)

        if matches:
            print(f"\n✅ Se encontraron {len(matches)} libro(s):")
            for i, book in enumerate(matches):
                print_book(book, i)
        else:
            print(f"\n❌ No se encontraron libros que coincidan con: {title}")
        return

    # -------------------------------
    # 3. BÚSQUEDA LINEAL POR AUTOR
    # -------------------------------
    elif option == "3":
        author = input("\nIngrese autor (coincidencia parcial): ").strip()

        # otra vez tu algoritmo lineal ⬇⬇⬇
        matches = linear_search_books(books, author=author)

        if matches:
            print(f"\n✅ Se encontraron {len(matches)} libro(s):")
            for i, book in enumerate(matches):
                print_book(book, i)
        else:
            print(f"\n❌ No se encontraron libros del autor: {author}")
        return

    else:
        print("\n❌ Opción no válida.")



def update_book_info():
    """Opción 4: Actualizar información de un libro"""
    print_header("ACTUALIZAR LIBRO")
    
    isbn = input("\nIngrese ISBN del libro a actualizar: ").strip()
    book = service_get_book_by_isbn(isbn)
    
    if not book:
        print(f"\n❌ No se encontró ningún libro con el ISBN: {isbn}")
        return
    
    print("\n📖 Libro actual:")
    print_book(book)
    
    print("\n¿Qué desea actualizar?")
    print("1. Título")
    print("2. Autor")
    print("3. Peso")
    print("4. Valor")
    print("5. Stock")
    print("6. Actualizar todo")
    
    option = input("\nSeleccione una opción: ").strip()
    
    try:
        if option == "1":
            new_title = input("Nuevo título: ").strip()
            if new_title:
                book.title = new_title
        
        elif option == "2":
            new_author = input("Nuevo autor: ").strip()
            if new_author:
                book.author = new_author
        
        elif option == "3":
            new_weight = float(input("Nuevo peso (kg): "))
            if new_weight > 0:
                book.weight = new_weight
        
        elif option == "4":
            new_value = int(input("Nuevo valor ($): "))
            if new_value >= 0:
                book.value = new_value
        
        elif option == "5":
            new_stock = int(input("Nuevo stock: "))
            if new_stock >= 0:
                book.stock = new_stock
        
        elif option == "6":
            new_title = input("Nuevo título: ").strip()
            new_author = input("Nuevo autor: ").strip()
            new_weight = float(input("Nuevo peso (kg): "))
            new_value = int(input("Nuevo valor ($): "))
            new_stock = int(input("Nuevo stock: "))
            
            if new_title and new_author and new_weight > 0 and new_value >= 0 and new_stock >= 0:
                book.title = new_title
                book.author = new_author
                book.weight = new_weight
                book.value = new_value
                book.stock = new_stock
        
        else:
            print("\n❌ Opción no válida")
            return
        
        result = service_update_book(book)
        
        if result:
            print("\n✅ Libro actualizado exitosamente")
            print_book(result)
        else:
            print("\n❌ No se pudo actualizar el libro")
    
    except ValueError:
        print("\n❌ Error: Ingrese valores numéricos válidos")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def manage_stock():
    """Opción 5: Gestionar stock"""
    print_header("GESTIONAR STOCK")
    
    isbn = input("\nIngrese ISBN del libro: ").strip()
    book = service_get_book_by_isbn(isbn)
    
    if not book:
        print(f"\n❌ No se encontró ningún libro con el ISBN: {isbn}")
        return
    
    print("\n📖 Libro encontrado:")
    print_book(book)
    
    print("\n¿Qué desea hacer?")
    print("1. Aumentar stock (entrada de inventario)")
    print("2. Disminuir stock (venta/préstamo)")
    
    option = input("\nSeleccione una opción: ").strip()
    
    try:
        amount = int(input("Ingrese cantidad: "))
        
        if amount <= 0:
            print("\n❌ La cantidad debe ser mayor a 0")
            return
        
        if option == "1":
            result = service_update_stock(isbn, amount)
        elif option == "2":
            result = service_update_stock(isbn, -amount)
        else:
            print("\n❌ Opción no válida")
            return
        
        if result:
            print("\n✅ Stock actualizado exitosamente")
            print_book(result)
        else:
            print("\n❌ No se pudo actualizar el stock")
    
    except ValueError:
        print("\n❌ Error: Ingrese un número válido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def delete_book():
    """Opción 6: Eliminar libro"""
    print_header("ELIMINAR LIBRO")
    
    isbn = input("\nIngrese ISBN del libro a eliminar: ").strip()
    book = service_get_book_by_isbn(isbn)
    
    if not book:
        print(f"\n❌ No se encontró ningún libro con el ISBN: {isbn}")
        return
    
    print("\n📖 Libro a eliminar:")
    print_book(book)
    
    confirm = input("\n⚠️  ¿Está seguro de eliminar este libro? (s/n): ").strip().lower()
    
    if confirm == "s":
        result = service_delete_book(isbn)
        if result:
            print("\n✅ Libro eliminado exitosamente del inventario")
        else:
            print("\n❌ No se pudo eliminar el libro")
    else:
        print("\n❌ Operación cancelada")


def view_available_books():
    """Opción 7: Ver libros disponibles"""
    print_header("LIBROS DISPONIBLES")
    
    books = service_get_available_books()
    
    if not books:
        print("\n📦 No hay libros disponibles en stock")
        return
    
    print(f"\nTotal de libros disponibles: {len(books)}")
    
    for i, book in enumerate(books):
        print_book(book, i)


def view_low_stock_books():
    """Opción 8: Ver libros con stock bajo"""
    print_header("LIBROS CON STOCK BAJO")
    
    try:
        threshold = int(input("\nIngrese el límite de stock (por defecto 5): ").strip() or "5")
        books = service_get_low_stock_books(threshold)
        
        if not books:
            print(f"\n✅ No hay libros con stock menor o igual a {threshold} unidades")
            return
        
        print(f"\n⚠️  Libros con stock ≤ {threshold} unidades: {len(books)}")
        
        for i, book in enumerate(books):
            print_book(book, i)
    
    except ValueError:
        print("\n❌ Error: Ingrese un número válido")


def show_reservation_queue():
    """Muestra la cola de reservas (FIFO) de un libro sin modificarla."""
    print_header("LISTA DE ESPERA DE UN LIBRO")

    isbn = input("ISBN del libro: ").strip()
    book = service_get_book_by_isbn(isbn)

    if not book:
        print("\n❌ El libro no existe.")
        return

    # Obtener una copia de la cola como lista
    reservations = book.reservations.toList()

    if not reservations:
        print("\n📭 No hay reservas para este libro.")
        return

    print(f"\n📚 Lista de espera para: {book.title}\n")

    for idx, r in enumerate(reservations, start=1):
        # r puede ser dict {"user_id": ..., "date": ...} o un string antiguo
        if isinstance(r, dict):
            user_id = r.get("user_id", "unknown")
            date = r.get("date", "unknown")
            print(f"{idx}. Usuario: {user_id} | Fecha de reserva: {date}")
        else:
            # caso viejo: solo el ID como string
            print(f"{idx}. Usuario: {r}")


def view_inventory_stats():
    """Opción 9: Ver estadísticas del inventario"""
    print_header("ESTADÍSTICAS DEL INVENTARIO")
    
    stats = service_get_inventory_stats()
    
    print(f"\n📊 Resumen del inventario:")
    print(f"\n   Total de libros diferentes: {stats['total_books']}")
    print(f"   Total de unidades en stock: {stats['total_stock']}")
    print(f"   Libros disponibles: {stats['available_books']}")
    print(f"   Libros sin stock: {stats['out_of_stock']}")
    print(f"   Valor total del inventario: ${stats['total_inventory_value']:,}")


def show_menu():
    """Muestra el menú principal"""
    print_header("SISTEMA DE GESTIÓN DE INVENTARIO")
    print("\n1. Agregar nuevo libro")
    print("2. Listar todos los libros")
    print("3. Listar todos los libros ordenados por isbn")
    print("4. Buscar libro")
    print("5. Actualizar información de libro")
    print("6. Gestionar stock")
    print("7. Eliminar libro")
    print("8. Ver libros disponibles")
    print("9. Ver libros con stock bajo")
    print("10. Ver estadísticas del inventario")
    print("11. Ver lista de espera de un libro")
    print("0. Salir")


def inventory_menu():
    """Función principal del menú de inventario"""
    while True:
        clear_screen()
        show_menu()
        
        option = input("\nSeleccione una opción: ").strip()
        
        if option == "1":
            add_book()
        elif option == "2":
            list_all_books()
        elif option == "3":
            list_books_sorted_by_isbn()
        elif option == "4":
            search_book()
        elif option == "5":
            update_book_info()
        elif option == "6":
            manage_stock()
        elif option == "7":
            delete_book()
        elif option == "8":
            view_available_books()
        elif option == "9":
            view_low_stock_books()
        elif option == "10":
            view_inventory_stats()
        elif option == "11":
            show_reservation_queue()   
        elif option == "0":
            print("\n👋 Regresando al menú principal...")
            break  # Sale del bucle y regresa al menú principal
        else:
            print("\n❌ Opción no válida. Por favor, seleccione una opción del menú.")
        
        pause()


if __name__ == "__main__":
    inventory_menu()