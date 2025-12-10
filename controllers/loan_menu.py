import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.loan_service import (
    create_loan,
    return_loan as service_return_loan,
    get_all_loans as service_get_all_loans,
    get_active_loans as service_get_active_loans,
    get_overdue_loans as service_get_overdue_loans,
    get_loans_by_user as service_get_loans_by_user,
    get_loans_by_book as service_get_loans_by_book,
    renew_loan as service_renew_loan,
    get_loan_statistics as service_get_loan_statistics
)

from services.book_service import get_book_by_isbn as service_get_book_by_isbn
from services.user_service import get_user_by_id as service_get_user_by_id
from services.book_service import update_book
from models.loan import Loan
from datetime import datetime


def clear_screen():
    print("\n" * 2)


def pause():
    input("\nPresiona Enter para continuar...")


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_loan(loan: Loan, index=None):
    prefix = f"[{index + 1}]" if index is not None else "→"
    status = "✅ Devuelto" if loan.returned else ("⚠️ Vencido" if loan.is_overdue() else "📖 Activo")

    print(f"\n{prefix} ID: {loan.loan_id[:8]}...")
    print(f"   Libro: {loan.book.title}")
    print(f"   Usuario: {loan.user.name}")
    print(f"   Fecha préstamo: {loan.loan_date.strftime('%Y-%m-%d')}")
    print(f"   Fecha vencimiento: {loan.expiration_date.strftime('%Y-%m-%d')}")

    if loan.returned:
        print(f"   Fecha devolución: {loan.return_date.strftime('%Y-%m-%d')}")
    else:
        if loan.is_overdue():
            print(f"   Días de retraso: {loan.days_overdue()}")
        else:
            print(f"   Días hasta vencimiento: {loan.days_until_due()}")

    print(f"   Estado: {status}")


# -------------------------------
#  Opción 1 - Crear préstamo
# -------------------------------
def option_create_loan():
    print_header("CREAR NUEVO PRÉSTAMO")

    isbn = input("\nIngrese ISBN del libro: ").strip()
    if not isbn:
        print("❌ ISBN vacío")
        return

    book = service_get_book_by_isbn(isbn)
    if not book:
        print("❌ Libro no encontrado")
        return

    print(f"\n📖 Libro: {book.title}")
    print(f"Stock disponible: {book.stock}")

    user_id = input("\nIngrese ID del usuario: ").strip()
    if not user_id:
        print("❌ ID vacío")
        return

    user = service_get_user_by_id(user_id)
    if not user:
        print("❌ Usuario no encontrado")
        return

    print(f"\n👤 Usuario: {user.name}")

    # SI NO HAY STOCK → Reserva automática
    if not book.isAvalible():
        print("\n⚠️ No hay stock → Reserva automática")

        if any(r == user_id for r in list(book.reservations.items)):
            print("❌ El usuario YA está en la cola")
            return

        book.reservations.enqueue({
            "user_id": user_id,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        
        update_book(book)

        print("📌 Usuario agregado a la cola FIFO.")
        return

    # SÍ HAY STOCK → préstamo normal
    days_input = input("\nDías de préstamo (14 por defecto): ").strip()
    try:
        days = int(days_input) if days_input else 14
    except:
        print("❌ Días inválidos")
        return

    confirm = input(f"\n¿Confirmar préstamo? (s/n): ").strip().lower()
    if confirm != "s":
        print("\n❌ Cancelado")
        return

    loan = create_loan(isbn, user_id, days)

    if loan:
        print("\n✅ Préstamo creado")
        print_loan(loan)
    else:
        print("\n❌ No se pudo crear")


# -------------------------------
#  Opción 2 - Devolver préstamo
# -------------------------------
def option_return_loan():
    print_header("DEVOLVER PRÉSTAMO")

    loans = service_get_active_loans()
    if not loans:
        print("\nNo hay préstamos activos.")
        return

    for i, ln in enumerate(loans):
        print_loan(ln, i)

    loan_id = input("\nID del préstamo a devolver: ").strip()
    if not loan_id:
        print("❌ ID vacío")
        return

    match = None
    for ln in loans:
        if ln.loan_id.startswith(loan_id) or ln.loan_id == loan_id:
            match = ln
            break

    if not match:
        print("❌ No encontrado")
        return

    print("\nPréstamo seleccionado:")
    print_loan(match)

    confirm = input("\n¿Confirmar devolución? (s/n): ").strip().lower()
    if confirm != "s":
        print("\n❌ Cancelado")
        return

    result = service_return_loan(match.loan_id)
    if result:
        print("\n✅ Devuelto correctamente")
    else:
        print("\n❌ No se pudo devolver")


# -------------------------------
#  Otras opciones
# -------------------------------
def option_list_active():
    print_header("PRÉSTAMOS ACTIVOS")
    loans = service_get_active_loans()
    if not loans:
        print("\nSin préstamos activos")
        return
    for i, ln in enumerate(loans):
        print_loan(ln, i)


def option_list_overdue():
    print_header("PRÉSTAMOS VENCIDOS")
    loans = service_get_overdue_loans()
    if not loans:
        print("\nNo hay vencidos")
        return
    for i, ln in enumerate(loans):
        print_loan(ln, i)


def option_list_all():
    print_header("HISTORIAL COMPLETO")
    loans = service_get_all_loans()
    if not loans:
        print("\nNo hay préstamos")
        return
    for i, ln in enumerate(loans):
        print_loan(ln, i)


def option_search_user():
    print_header("PRÉSTAMOS POR USUARIO")
    user_id = input("ID: ").strip()
    user = service_get_user_by_id(user_id)
    if not user:
        print("Usuario no existe")
        return
    loans = service_get_loans_by_user(user_id)
    for i, ln in enumerate(loans):
        print_loan(ln, i)


def option_search_book():
    print_header("PRÉSTAMOS POR LIBRO")
    isbn = input("ISBN: ").strip()
    book = service_get_book_by_isbn(isbn)
    if not book:
        print("Libro no existe")
        return
    loans = service_get_loans_by_book(isbn)
    for i, ln in enumerate(loans):
        print_loan(ln, i)


def option_renew():
    print_header("RENOVAR PRÉSTAMO")

    loans = service_get_active_loans()
    if not loans:
        print("\nNo hay activos")
        return

    for i, ln in enumerate(loans):
        print_loan(ln, i)

    loan_id = input("\nID del préstamo: ").strip()

    match = None
    for ln in loans:
        if ln.loan_id.startswith(loan_id) or ln.loan_id == loan_id:
            match = ln
            break

    if not match:
        print("No encontrado")
        return

    days_input = input("Días adicionales (14 por defecto): ").strip()
    try:
        days = int(days_input) if days_input else 14
    except:
        print("Inválido")
        return

    confirm = input("¿Confirmar? (s/n): ").strip().lower()
    if confirm != "s":
        print("Cancelado")
        return

    result = service_renew_loan(match.loan_id, days)
    if result:
        print("\nRenovado")
        print_loan(result)


def option_statistics():
    print_header("ESTADÍSTICAS")
    stats = service_get_loan_statistics()

    print(f"\nTotal: {stats['total_loans']}")
    print(f"Activos: {stats['active_loans']}")
    print(f"Devueltos: {stats['returned_loans']}")
    print(f"Vencidos: {stats['overdue_loans']}")


# -------------------------------
#  MENÚ PRINCIPAL
# -------------------------------
def show_menu():
    print_header("SISTEMA DE PRÉSTAMOS")
    print("1. Crear préstamo")
    print("2. Devolver préstamo")
    print("3. Listar activos")
    print("4. Listar vencidos")
    print("5. Historial completo")
    print("6. Buscar por usuario")
    print("7. Buscar por libro")
    print("8. Renovar préstamo")
    print("9. Ver estadísticas")
    print("0. Salir")


def loan_menu():
    while True:
        clear_screen()
        show_menu()
        option = input("\nSeleccione una opción: ").strip()

        if option == "1":
            option_create_loan()
        elif option == "2":
            option_return_loan()
        elif option == "3":
            option_list_active()
        elif option == "4":
            option_list_overdue()
        elif option == "5":
            option_list_all()
        elif option == "6":
            option_search_user()
        elif option == "7":
            option_search_book()
        elif option == "8":
            option_renew()
        elif option == "9":
            option_statistics()
        elif option == "0":
            print("\n👋 Regresando...")
            break
        else:
            print("❌ Opción inválida")

        pause()


if __name__ == "__main__":
    loan_menu()
