import sys
from ui.inventory_menu import inventory_menu
from ui.shelf_menu import shelf_menu  # Cuando lo crees
from ui.loan_menu import loan_menu  # Si ya existe
from ui.user_menu import user_menu  # Si ya existe


def clear_screen():
    """Limpia la consola"""
    print("\n" * 2)


def show_main_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("  SISTEMA DE GESTIÓN DE BIBLIOTECA")
    print("=" * 60)
    print("\n1. Gestión de Inventario (Libros)")
    print("2. Gestión de Estantes")
    print("3. Gestión de Préstamos")
    print("4. Gestión de Usuarios")
    print("0. Salir")


def main():
    """Función principal del sistema"""
    while True:
        clear_screen()
        show_main_menu()
        
        option = input("\nSeleccione una opción: ").strip()
        
        if option == "1":
            inventory_menu()  # Llama al menú de inventario
        elif option == "2":
            # shelf_menu()  # Llama al menú de estantes (cuando lo crees)
            print("\n⚠️ Menú de estantes en desarrollo...")
            input("\nPresiona Enter para continuar...")
        elif option == "3":
            # loan_menu()  # Llama al menú de préstamos
            print("\n⚠️ Menú de préstamos en desarrollo...")
            input("\nPresiona Enter para continuar...")
        elif option == "4":
            # user_menu()  # Llama al menú de usuarios
            print("\n⚠️ Menú de usuarios en desarrollo...")
            input("\nPresiona Enter para continuar...")
        elif option == "0":
            print("\n👋 ¡Gracias por usar el Sistema de Gestión de Biblioteca!")
            sys.exit(0)
        else:
            print("\n❌ Opción no válida. Por favor, seleccione una opción del menú.")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()