import sys

from controllers.inventory_menu import inventory_menu
from controllers.shelf_menu import shelf_menu
from controllers.loan_menu import loan_menu
from controllers.user_menu import user_menu
from controllers.report_menu import reports_menu


def clear_screen():
    """Limpia la consola."""
    print("\n" * 2)


def show_main_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 60)
    print("  SISTEMA DE GESTIÓN DE BIBLIOTECA")
    print("=" * 60)
    print("\n1. Gestión de Inventario (Libros)")
    print("2. Gestión de Estantes")
    print("3. Gestión de Préstamos")
    print("4. Gestión de Usuarios")
    print("5. Reportes")    
    print("0. Salir")


def main():
    print("MAIN EJECUTANDOSE")

    """Función principal del sistema."""
    while True:
        clear_screen()
        show_main_menu()

        option = input("\nSeleccione una opción: ").strip()

        if option == "1":
            inventory_menu()

        elif option == "2":
            shelf_menu()

        elif option == "3":
            loan_menu()

        elif option == "4":
            user_menu()

        elif option == "5":        
            reports_menu()

        elif option == "0":
            print("\n👋 ¡Gracias por usar el Sistema de Gestión de Biblioteca!")
            sys.exit(0)

        else:
            print("\n❌ Opción no válida. Por favor seleccione una opción del menú.")
            input("\nPresiona Enter para continuar...")



