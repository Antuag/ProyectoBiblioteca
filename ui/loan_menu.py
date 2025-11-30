import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.loan_service import (
    create_loan as service_create_loan,
    return_loan as service_return_loan,
    get_all_loans as service_get_all_loans,
    get_active_loans as service_get_active_loans,
    get_overdue_loans as service_get_overdue_loans,
    get_loans_by_user as service_get_loans_by_user,
    get_loans_by_book as service_get_loans_by_book,
    get_loan_by_id as service_get_loan_by_id,
    renew_loan as service_renew_loan,
    get_loan_statistics as service_get_loan_statistics
)
from services.book_service import get_book_by_isbn as service_get_book_by_isbn
from services.user_service import get_user_by_id as service_get_user_by_id
from models.loan import Loan


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


def print_loan(loan: Loan, index=None):
    """Imprime la información de un préstamo de forma formateada"""
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


def create_loan():
    """Opción 1: Crear un nuevo préstamo"""
    print_header("CREAR NUEVO PRÉSTAMO")
    
    # Solicitar ISBN del libro
    isbn = input("\nIngrese ISBN del libro: ").strip()
    if not isbn:
        print("❌ El ISBN no puede estar vacío")
        return
    
    # Verificar que el libro existe
    book = service_get_book_by_isbn(isbn)
    if not book:
        print(f"❌ No se encontró un libro con el ISBN: {isbn}")
        return
    
    print(f"\n📖 Libro: {book.title}")
    print(f"   Autor: {book.author}")
    print(f"   Stock disponible: {book.stock}")
    
    if not book.isAvalible():
        print("\n❌ Este libro no tiene stock disponible")
        return
    
    # Solicitar ID del usuario
    user_id = input("\nIngrese ID del usuario: ").strip()
    if not user_id:
        print("❌ El ID del usuario no puede estar vacío")
        return
    
    # Verificar que el usuario existe
    user = service_get_user_by_id(user_id)
    if not user:
        print(f"❌ No se encontró un usuario con el ID: {user_id}")
        return
    
    print(f"\n👤 Usuario: {user.name}")
    print(f"   Préstamos activos: {len(user.loans)}")
    
    if not user.can_borrow():
        print("\n❌ Este usuario ha alcanzado el límite de préstamos activos (máximo 3)")
        return
    
    # Solicitar días de préstamo
    try:
        days_input = input("\nIngrese días de préstamo (por defecto 14): ").strip()
        days = int(days_input) if days_input else 14
        
        if days <= 0:
            print("❌ Los días deben ser mayor a 0")
            return
    except ValueError:
        print("❌ Ingrese un número válido de días")
        return
    
    # Confirmar
    confirm = input(f"\n¿Confirmar préstamo de '{book.title}' a '{user.name}' por {days} días? (s/n): ").strip().lower()
    
    if confirm == "s":
        loan = service_create_loan(isbn, user_id, days)
        
        if loan:
            print("\n✅ Préstamo creado exitosamente")
            print_loan(loan)
        else:
            print("\n❌ No se pudo crear el préstamo")
    else:
        print("\n❌ Operación cancelada")


def return_loan():
    """Opción 2: Devolver un préstamo"""
    print_header("DEVOLVER PRÉSTAMO")
    
    # Mostrar préstamos activos primero
    active_loans = service_get_active_loans()
    
    if not active_loans:
        print("\n📦 No hay préstamos activos para devolver")
        return
    
    print(f"\nPréstamos activos ({len(active_loans)}):")
    for i, loan in enumerate(active_loans):
        print_loan(loan, i)
    
    # Solicitar ID del préstamo
    loan_id = input("\nIngrese ID del préstamo a devolver: ").strip()
    if not loan_id:
        print("❌ El ID no puede estar vacío")
        return
    
    # Buscar el préstamo completo si solo pusieron el ID corto
    loan_to_return = None
    for loan in active_loans:
        if loan.loan_id.startswith(loan_id) or loan.loan_id == loan_id:
            loan_to_return = loan
            break
    
    if not loan_to_return:
        print(f"❌ No se encontró un préstamo activo con el ID: {loan_id}")
        return
    
    print(f"\n📖 Préstamo a devolver:")
    print_loan(loan_to_return)
    
    # Verificar si está vencido
    if loan_to_return.is_overdue():
        print(f"\n⚠️  ATENCIÓN: Este préstamo está vencido por {loan_to_return.days_overdue()} días")
    
    confirm = input("\n¿Confirmar devolución? (s/n): ").strip().lower()
    
    if confirm == "s":
        result = service_return_loan(loan_to_return.loan_id)
        
        if result:
            print("\n✅ Préstamo devuelto exitosamente")
            print(f"   Libro devuelto: {result.book.title}")
            print(f"   Usuario: {result.user.name}")
            print(f"   Fecha devolución: {result.return_date.strftime('%Y-%m-%d')}")
        else:
            print("\n❌ No se pudo devolver el préstamo")
    else:
        print("\n❌ Operación cancelada")


def list_active_loans():
    """Opción 3: Listar préstamos activos"""
    print_header("PRÉSTAMOS ACTIVOS")
    
    loans = service_get_active_loans()
    
    if not loans:
        print("\n📦 No hay préstamos activos")
        return
    
    print(f"\nTotal de préstamos activos: {len(loans)}")
    
    for i, loan in enumerate(loans):
        print_loan(loan, i)


def list_overdue_loans():
    """Opción 4: Listar préstamos vencidos"""
    print_header("PRÉSTAMOS VENCIDOS")
    
    loans = service_get_overdue_loans()
    
    if not loans:
        print("\n✅ No hay préstamos vencidos")
        return
    
    print(f"\n⚠️  Total de préstamos vencidos: {len(loans)}")
    
    for i, loan in enumerate(loans):
        print_loan(loan, i)


def list_all_loans():
    """Opción 5: Listar todos los préstamos"""
    print_header("HISTORIAL DE PRÉSTAMOS")
    
    loans = service_get_all_loans()
    
    if not loans:
        print("\n📦 No hay préstamos registrados")
        return
    
    print(f"\nTotal de préstamos: {len(loans)}")
    
    for i, loan in enumerate(loans):
        print_loan(loan, i)


def search_loans_by_user():
    """Opción 6: Buscar préstamos por usuario"""
    print_header("PRÉSTAMOS POR USUARIO")
    
    user_id = input("\nIngrese ID del usuario: ").strip()
    if not user_id:
        print("❌ El ID no puede estar vacío")
        return
    
    # Verificar que el usuario existe
    user = service_get_user_by_id(user_id)
    if not user:
        print(f"❌ No se encontró un usuario con el ID: {user_id}")
        return
    
    print(f"\n👤 Usuario: {user.name}")
    
    loans = service_get_loans_by_user(user_id)
    
    if not loans:
        print("\n📦 Este usuario no tiene préstamos registrados")
        return
    
    print(f"\nTotal de préstamos: {len(loans)}")
    active = sum(1 for loan in loans if not loan.returned)
    print(f"Activos: {active} | Devueltos: {len(loans) - active}")
    
    for i, loan in enumerate(loans):
        print_loan(loan, i)


def search_loans_by_book():
    """Opción 7: Buscar préstamos por libro"""
    print_header("PRÉSTAMOS POR LIBRO")
    
    isbn = input("\nIngrese ISBN del libro: ").strip()
    if not isbn:
        print("❌ El ISBN no puede estar vacío")
        return
    
    # Verificar que el libro existe
    book = service_get_book_by_isbn(isbn)
    if not book:
        print(f"❌ No se encontró un libro con el ISBN: {isbn}")
        return
    
    print(f"\n📖 Libro: {book.title}")
    print(f"   Autor: {book.author}")
    
    loans = service_get_loans_by_book(isbn)
    
    if not loans:
        print("\n📦 Este libro no tiene préstamos registrados")
        return
    
    print(f"\nTotal de préstamos: {len(loans)}")
    active = sum(1 for loan in loans if not loan.returned)
    print(f"Activos: {active} | Devueltos: {len(loans) - active}")
    
    for i, loan in enumerate(loans):
        print_loan(loan, i)


def renew_loan():
    """Opción 8: Renovar un préstamo"""
    print_header("RENOVAR PRÉSTAMO")
    
    # Mostrar préstamos activos
    active_loans = service_get_active_loans()
    
    if not active_loans:
        print("\n📦 No hay préstamos activos para renovar")
        return
    
    print(f"\nPréstamos activos ({len(active_loans)}):")
    for i, loan in enumerate(active_loans):
        print_loan(loan, i)
    
    # Solicitar ID del préstamo
    loan_id = input("\nIngrese ID del préstamo a renovar: ").strip()
    if not loan_id:
        print("❌ El ID no puede estar vacío")
        return
    
    # Buscar el préstamo
    loan_to_renew = None
    for loan in active_loans:
        if loan.loan_id.startswith(loan_id) or loan.loan_id == loan_id:
            loan_to_renew = loan
            break
    
    if not loan_to_renew:
        print(f"❌ No se encontró un préstamo activo con el ID: {loan_id}")
        return
    
    print(f"\n📖 Préstamo a renovar:")
    print_loan(loan_to_renew)
    
    # Solicitar días adicionales
    try:
        days_input = input("\nIngrese días adicionales (por defecto 14): ").strip()
        days = int(days_input) if days_input else 14
        
        if days <= 0:
            print("❌ Los días deben ser mayor a 0")
            return
    except ValueError:
        print("❌ Ingrese un número válido de días")
        return
    
    confirm = input(f"\n¿Confirmar renovación por {days} días adicionales? (s/n): ").strip().lower()
    
    if confirm == "s":
        result = service_renew_loan(loan_to_renew.loan_id, days)
        
        if result:
            print("\n✅ Préstamo renovado exitosamente")
            print_loan(result)
        else:
            print("\n❌ No se pudo renovar el préstamo")
    else:
        print("\n❌ Operación cancelada")


def view_loan_statistics():
    """Opción 9: Ver estadísticas de préstamos"""
    print_header("ESTADÍSTICAS DE PRÉSTAMOS")
    
    stats = service_get_loan_statistics()
    
    print(f"\n📊 Resumen de préstamos:")
    print(f"\n   Total de préstamos: {stats['total_loans']}")
    print(f"   Préstamos activos: {stats['active_loans']}")
    print(f"   Préstamos devueltos: {stats['returned_loans']}")
    print(f"   Préstamos vencidos: {stats['overdue_loans']}")
    print(f"   Préstamos al día: {stats['on_time_loans']}")
    
    if stats['active_loans'] > 0:
        overdue_percentage = (stats['overdue_loans'] / stats['active_loans']) * 100
        print(f"\n   Porcentaje de mora: {overdue_percentage:.1f}%")


def show_menu():
    """Muestra el menú principal de préstamos"""
    print_header("SISTEMA DE GESTIÓN DE PRÉSTAMOS")
    print("\n1. Crear nuevo préstamo")
    print("2. Devolver préstamo")
    print("3. Listar préstamos activos")
    print("4. Listar préstamos vencidos")
    print("5. Ver historial de préstamos")
    print("6. Buscar préstamos por usuario")
    print("7. Buscar préstamos por libro")
    print("8. Renovar préstamo")
    print("9. Ver estadísticas de préstamos")
    print("0. Salir")


def loan_menu():
    """Función principal del menú de préstamos"""
    while True:
        clear_screen()
        show_menu()
        
        option = input("\nSeleccione una opción: ").strip()
        
        if option == "1":
            create_loan()
        elif option == "2":
            return_loan()
        elif option == "3":
            list_active_loans()
        elif option == "4":
            list_overdue_loans()
        elif option == "5":
            list_all_loans()
        elif option == "6":
            search_loans_by_user()
        elif option == "7":
            search_loans_by_book()
        elif option == "8":
            renew_loan()
        elif option == "9":
            view_loan_statistics()
        elif option == "0":
            print("\n👋 Regresando al menú principal...")
            break
        else:
            print("\n❌ Opción no válida. Por favor, seleccione una opción del menú.")
        
        pause()


if __name__ == "__main__":
    loan_menu()