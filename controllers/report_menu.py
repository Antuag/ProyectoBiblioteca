import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Algoritmos ---
from algorithms.merge_sort import merge_sort_pairs
from algorithms.report_recursive import recursive_show_stack, recursive_show_queue
from algorithms.backtracking_shelf import optimal_shelf_backtracking, MAX_WEIGHT

# --- Servicios ---
from services.book_service import get_all_books, get_book_by_isbn, _book_to_dict
from services.loan_service import get_loans_by_user

# --- Estructuras ---
from structures.stack import Stack
from structures.queue import Queue
from services.history_service import get_user_history_stack
from algorithms.merge_sort import merge_sort_books_by_value



#  FUNCIONES DE UI

def print_header(title):
    """Muestra un encabezado estético para cada sección."""
    print("\n" + "=" * 60)
    print(f"   {title}")
    print("=" * 60)


def pause():
    input("\nPresiona Enter para continuar...")


#  REPORTE A — LIBROS ORDENADOS (MERGE SORT)

def report_sorted_books():
    """
    Muestra todos los libros ordenados alfabéticamente.

    IMPORTANTE:
    merge_sort no puede ordenar objetos directamente,
    por eso convertimos cada libro al formato:

        (titulo_en_minusculas, libro)
    """

    print_header("REPORTE A — LIBROS ORDENADOS (MERGE SORT)")

    books = get_all_books()
    if not books:
        print("\n❌ No hay libros en el sistema.")
        return

    # Convertimos a pares ordenables
    sortable = [(bk.title.lower(), bk) for bk in books]

    # Ordenamos usando merge_sort
    sorted_pairs = merge_sort_pairs(sortable)

    print("\n📚 Libros ordenados:\n")
    for (_, book) in sorted_pairs:
        print(f"- {book.title} | {book.author}")

    pause()


#  REPORTE B — HISTORIAL DE PRÉSTAMOS (PILA + RECURSIÓN)

def report_loan_history():
    """Muestra el historial de préstamos de un usuario usando una pila."""

    print_header("REPORTE B — HISTORIAL DE PRÉSTAMOS (PILA + RECURSIÓN)")

    user_id = input("ID del usuario: ").strip()
    loans = get_loans_by_user(user_id)

    if not loans:
        print("\n❌ Este usuario no tiene préstamos.")
        return

    stack = Stack()
    for ln in loans:
        stack.push(ln)

    print("\nHistorial de préstamos:\n")
    recursive_show_stack(stack)

    pause()


#  REPORTE C — RESERVAS (COLA + RECURSIÓN)

def report_reservations():
    print_header("REPORTE C — RESERVAS (COLA + RECURSIÓN)")

    isbn = input("ISBN del libro: ").strip()
    book = get_book_by_isbn(isbn)

    if not book:
        print("\n❌ El libro no existe.")
        return

    if book.reservations.is_empty():
        print("\nEste libro no tiene reservas.")
        return

    print("\nReservas registradas:\n")
    recursive_show_queue(book.reservations)

    pause()


def recursive_show_queue(queue):
    """Imprime una cola sin modificar su orden."""
    if queue.is_empty():
        return

    item = queue.dequeue()
    print(f"- Usuario: {item['user_id']} | Fecha: {item['date']}")

    recursive_show_queue(queue)

    queue.enqueue(item)


def report_lifo_history():
    """
    Muestra el historial LIFO persistente de un usuario usando una Pila
    almacenada en data/history.json
    """
    print_header("REPORTE EXTRA — HISTORIAL LIFO (PILA PERSISTENTE)")

    user_id = input("ID del usuario: ").strip()

    # Cargar la pila desde history.json
    stack = get_user_history_stack(user_id)

    if stack.is_empty():
        print("\n❌ Este usuario no tiene historial LIFO registrado.")
        return

    print("\nHistorial LIFO del usuario:\n")
    recursive_show_stack(stack)

    pause()
    
    
def report_books_sorted_by_value():
    print_header("REPORTE GLOBAL — LIBROS ORDENADOS POR VALOR (MERGE SORT)")

    books = get_all_books()

    if not books:
        print("\n📦 No hay libros en el inventario")
        return

    sorted_books = merge_sort_books_by_value(books)

    print(f"\nTotal de libros: {len(sorted_books)}")
    for i, book in enumerate(sorted_books):
        print(book, i)

    # Guardar archivo
    import json, os
    report_path = os.path.join("data", "report_sorted_by_value.json")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump([_book_to_dict(b) for b in sorted_books], f, indent=4, ensure_ascii=False)

    pause()


def report_optimal_shelf():
    """Reporte de estantería óptima (Backtracking)"""
    print_header("REPORTE — ESTANTERÍA ÓPTIMA (BACKTRACKING)")
    books = get_all_books()
    if not books:
        print("\n❌ No hay libros en el sistema.")
        return
    result, total_value = optimal_shelf_backtracking(books)
    if not result:
        print("\n❌ No hay combinación posible dentro del peso máximo.")
        return
    print(f"\nLibros seleccionados (máx {MAX_WEIGHT} kg):")
    for book in result:
        print(f"- {book.title} | {book.author} | {book.weight} kg | ${book.value}")
    print(f"\nValor total: ${total_value}")
    print(f"Peso total: {sum(b.weight for b in result):.2f} kg")
    pause()


#  MENÚ PRINCIPAL DE REPORTES

def show_reporting_menu():
    print_header("MENÚ DE REPORTES")
    print("1. Libros ordenados (Merge Sort)")
    print("2. Historial de préstamos (Pila + Recursión)")
    print("3. Reservas de un libro (Cola + Recursión)")
    print("4. Historial LIFO (Pila persistente)")
    print("5. Libros ordenados por valor COP")
    print("6. Estantería óptima (Backtracking)")
    print("0. Volver al menú principal")


def reports_menu():
    """Controla el flujo del menú de reportes."""
    while True:
        show_reporting_menu()
        op = input("\nSeleccione una opción: ").strip()

        if op == "1":
            report_sorted_books()
        elif op == "2":
            report_loan_history()
        elif op == "3":
            report_reservations()
        elif op == "4":
            report_lifo_history()
        elif op == "5":
            report_books_sorted_by_value()
        elif op == "6":
            report_optimal_shelf()
        elif op == "0":
            print("\nRegresando al menú principal...")
            break
        else:
            print("\n❌ Opción no válida.")
            pause()

