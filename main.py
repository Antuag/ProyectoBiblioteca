import sys
from ui.inventory_menu import inventory_menu
from ui.shelf_menu import shelf_menu
from ui.loan_menu import loan_menu
from ui.user_menu import user_menu


def clear_screen():
    """Limpia la consola"""
    print("\n" * 2)


def print_banner():
    """Imprime el banner del sistema"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          SISTEMA DE GESTIÓN DE BIBLIOTECA                   ║
    ║                                                              ║
    ║                    Proyecto Biblioteca                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def show_main_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("  MENÚ PRINCIPAL")
    print("=" * 60)
    print("\n📚 GESTIÓN DE RECURSOS")
    print("   1. Gestión de Inventario (Libros)")
    print("   2. Gestión de Estantes")
    print("\n👥 GESTIÓN DE SERVICIOS")
    print("   3. Gestión de Préstamos")
    print("   4. Gestión de Usuarios")
    print("\n❓ AYUDA Y CONFIGURACIÓN")
    print("   5. Ayuda y documentación")
    print("   6. Acerca del sistema")
    print("\n   0. Salir del sistema")
    print("=" * 60)


def show_help():
    """Muestra la ayuda del sistema"""
    clear_screen()
    print("\n" + "=" * 60)
    print("  AYUDA Y DOCUMENTACIÓN")
    print("=" * 60)
    
    help_text = """
    📚 GESTIÓN DE INVENTARIO (LIBROS)
       - Agregar, actualizar y eliminar libros
       - Buscar libros por ISBN, título o autor
       - Gestionar stock de libros
       - Ver estadísticas del inventario
    
    📦 GESTIÓN DE ESTANTES
       - Crear y eliminar estantes
       - Agregar libros a estantes físicos
       - Remover y reemplazar libros en estantes
       - Buscar ubicación física de libros
       - Ver ocupación de estantes
       
       RESTRICCIONES:
       • Cada estante tiene 5 filas con 4 espacios cada una (20 libros)
       • Cada fila soporta máximo 8 kg de peso
       • Los libros se colocan automáticamente en la primera fila disponible
    
    📖 GESTIÓN DE PRÉSTAMOS
       - Crear préstamos de libros
       - Devolver libros prestados
       - Renovar préstamos activos
       - Ver préstamos vencidos
       - Buscar préstamos por usuario o libro
       
       REGLAS:
       • Duración por defecto: 14 días
       • Máximo 3 préstamos por usuario
       • Al prestar se reduce el stock automáticamente
       • Al devolver se incrementa el stock automáticamente
    
    👤 GESTIÓN DE USUARIOS
       - Registrar nuevos usuarios
       - Actualizar información de usuarios
       - Ver historial de préstamos por usuario
       - Ver estadísticas de usuarios
    
    💡 CONSEJOS:
       - Los datos se guardan automáticamente en archivos JSON
       - Puedes buscar por texto parcial en títulos, autores y nombres
       - Las fechas se manejan en formato YYYY-MM-DD
       - Los préstamos vencidos se marcan automáticamente
    """
    
    print(help_text)
    input("\nPresiona Enter para volver al menú principal...")


def show_about():
    """Muestra información del sistema"""
    clear_screen()
    print("\n" + "=" * 60)
    print("  ACERCA DEL SISTEMA")
    print("=" * 60)
    
    about_text = """
    📚 SISTEMA DE GESTIÓN DE BIBLIOTECA
    
    Versión: 1.0.0
    
    DESCRIPCIÓN:
    Sistema completo para la gestión de una biblioteca que permite
    administrar inventario de libros, ubicación física en estantes,
    préstamos a usuarios y control de devoluciones.
    
    CARACTERÍSTICAS:
    ✅ Gestión completa de inventario de libros
    ✅ Control de ubicación física en estantes
    ✅ Sistema de préstamos y devoluciones
    ✅ Gestión de usuarios y su historial
    ✅ Control automático de stock
    ✅ Detección de préstamos vencidos
    ✅ Estadísticas y reportes
    ✅ Persistencia de datos en JSON
    
    TECNOLOGÍAS:
    • Python 3.x
    • Estructuras de datos (Pilas, Colas)
    • Almacenamiento en JSON
    • Programación Orientada a Objetos
    
    MÓDULOS:
    • models/     - Modelos de datos (Book, Shelf, Loan, User)
    • services/   - Lógica de negocio y persistencia
    • ui/         - Interfaces de usuario (menús)
    • structures/ - Estructuras de datos (Stack, Queue)
    • data/       - Archivos JSON de almacenamiento
    
    DESARROLLADO PARA:
    Proyecto de Técnicas de Programación
    Universidad de Caldas
    """
    
    print(about_text)
    input("\nPresiona Enter para volver al menú principal...")


def main():
    """Función principal del sistema"""
    while True:
        clear_screen()
        print_banner()
        show_main_menu()
        
        option = input("\n👉 Seleccione una opción: ").strip()
        
        if option == "1":
            # Gestión de Inventario (Libros)
            inventory_menu()
        
        elif option == "2":
            # Gestión de Estantes
            shelf_menu()
        
        elif option == "3":
            # Gestión de Préstamos
            loan_menu()
        
        elif option == "4":
            # Gestión de Usuarios
            user_menu()
        
        elif option == "5":
            # Ayuda
            show_help()
        
        elif option == "6":
            # Acerca del sistema
            show_about()
        
        elif option == "0":
            # Salir
            clear_screen()
            print("\n" + "=" * 60)
            print("  GRACIAS POR USAR EL SISTEMA DE GESTIÓN DE BIBLIOTECA")
            print("=" * 60)
            print("\n  📚 Todos los datos han sido guardados correctamente")
            print("  👋 ¡Hasta pronto!\n")
            sys.exit(0)
        
        else:
            print("\n❌ Opción no válida. Por favor, seleccione una opción del menú.")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Manejar Ctrl+C
        print("\n\n👋 Sistema cerrado por el usuario. ¡Hasta pronto!")
        sys.exit(0)
    except Exception as e:
        # Manejar errores inesperados
        print(f"\n\n❌ Error crítico del sistema: {e}")
        print("Por favor, contacte al administrador del sistema.")
        sys.exit(1)