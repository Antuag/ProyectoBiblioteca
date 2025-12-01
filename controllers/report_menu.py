import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Algoritmos ---
from algorithms.merge_sort import merge_sort_pairs
from algorithms.report_utils import recursive_show_stack, recursive_show_queue

# --- Servicios ---
from services.book_service import get_all_books, get_book_by_isbn
from services.loan_service import get_loans_by_user

# --- Estructuras ---
from structures.stack import Stack
from structures.queue import Queue


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
    """Muestra las reservas de un libro usando una cola."""

    print_header("REPORTE C — RESERVAS (COLA + RECURSIÓN)")

    isbn = input("ISBN del libro: ").strip()
    book = get_book_by_isbn(isbn)

    if not book:
        print("\n❌ El libro no existe.")
        return

    if book.reservations.is_empty():
        print("\nEste libro no tiene reservas.")
        return

    # Copia temporal para no alterar la cola original
    temp = Queue()

    while not book.reservations.is_empty():
        usuario = book.reservations.dequeue()
        temp.enqueue(usuario)
        book.reservations.enqueue(usuario)  # volver a ponerlo

    print("\nReservas registradas:\n")
    recursive_show_queue(temp)

    pause()


#  MENÚ PRINCIPAL DE REPORTES

def show_reporting_menu():
    print_header("MENÚ DE REPORTES")
    print("1. Libros ordenados (Merge Sort)")
    print("2. Historial de préstamos (Pila + Recursión)")
    print("3. Reservas de un libro (Cola + Recursión)")
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
        elif op == "0":
            print("\nRegresando al menú principal...")
            break
        else:
            print("\n❌ Opción no válida.")
            pause()
