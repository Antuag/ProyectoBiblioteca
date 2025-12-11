import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import (
    create_user as service_create_user,
    update_user as service_update_user,
    get_all_users as service_get_all_users,
    get_user_by_id as service_get_user_by_id,
    delete_user as service_delete_user,
    search_users_by_name as service_search_users_by_name,
    get_users_with_active_loans as service_get_users_with_active_loans,
    get_user_statistics as service_get_user_statistics
)
from services.loan_service import get_loans_by_user as service_get_loans_by_user
from models.user import User


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


def print_user(user: User, index=None):
    """Imprime la información de un usuario de forma formateada"""
    prefix = f"[{index + 1}]" if index is not None else "→"
    
    print(f"\n{prefix} ID: {user.id}")
    print(f"   Nombre: {user.name}")
    if user.email:
        print(f"   Email: {user.email}")
    if user.phone:
        print(f"   Teléfono: {user.phone}")
    print(f"   Préstamos activos: {len(user.loans)}")
    print(f"   Estado: {'🔴 Con préstamos' if user.has_active_loans() else '🟢 Sin préstamos'}")


def add_user():
    """Opción 1: Agregar un nuevo usuario"""
    print_header("AGREGAR NUEVO USUARIO")
    
    try:
        user_id = input("\nIngrese ID del usuario: ").strip()
        if not user_id:
            print("❌ El ID no puede estar vacío")
            return
        
        # Verificar si ya existe
        existing_user = service_get_user_by_id(user_id)
        if existing_user:
            print(f"❌ Ya existe un usuario con el ID: {user_id}")
            return
        
        name = input("Ingrese nombre completo: ").strip()
        if not name:
            print("❌ El nombre no puede estar vacío")
            return
        
        email = input("Ingrese email (opcional, Enter para omitir): ").strip()
        email = email if email else None
        
        phone = input("Ingrese teléfono (opcional, Enter para omitir): ").strip()
        phone = phone if phone else None
        
        # Crear el usuario
        new_user = User(user_id, name, email, phone)
        result = service_create_user(new_user)
        
        if result:
            print("\n✅ Usuario agregado exitosamente")
            print_user(new_user)
        else:
            print("\n❌ No se pudo agregar el usuario")
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def list_all_users():
    """Opción 2: Listar todos los usuarios"""
    print_header("TODOS LOS USUARIOS")
    
    users = service_get_all_users()
    
    if not users:
        print("\n📦 No hay usuarios registrados")
        return
    
    print(f"\nTotal de usuarios: {len(users)}")
    
    for i, user in enumerate(users):
        print_user(user, i)


def search_user():
    """Opción 3: Buscar usuario"""
    print_header("BUSCAR USUARIO")
    
    print("\n¿Cómo desea buscar?")
    print("1. Por ID")
    print("2. Por nombre")
    
    option = input("\nSeleccione una opción: ").strip()
    
    if option == "1":
        user_id = input("\nIngrese ID del usuario: ").strip()
        user = service_get_user_by_id(user_id)
        
        if user:
            print("\n✅ Usuario encontrado:")
            print_user(user)
            
            # Mostrar préstamos si tiene
            if user.has_active_loans():
                print(f"\n📚 Préstamos activos ({len(user.loans)}):")
                loans = service_get_loans_by_user(user_id)
                for i, loan in enumerate(loans):
                    if not loan.returned:
                        print(f"\n   [{i + 1}] {loan.book.title}")
                        print(f"       Vence: {loan.expiration_date.strftime('%Y-%m-%d')}")
                        if loan.is_overdue():
                            print(f"       ⚠️ VENCIDO - {loan.days_overdue()} días de retraso")
        else:
            print(f"\n❌ No se encontró ningún usuario con el ID: {user_id}")
    
    elif option == "2":
        name = input("\nIngrese nombre (búsqueda parcial): ").strip()
        users = service_search_users_by_name(name)
        
        if users:
            print(f"\n✅ Se encontraron {len(users)} usuario(s):")
            for i, user in enumerate(users):
                print_user(user, i)
        else:
            print(f"\n❌ No se encontraron usuarios con el nombre: {name}")
    
    else:
        print("\n❌ Opción no válida")


def update_user_info():
    """Opción 4: Actualizar información de un usuario"""
    print_header("ACTUALIZAR USUARIO")
    
    user_id = input("\nIngrese ID del usuario a actualizar: ").strip()
    user = service_get_user_by_id(user_id)
    
    if not user:
        print(f"\n❌ No se encontró ningún usuario con el ID: {user_id}")
        return
    
    print("\n👤 Usuario actual:")
    print_user(user)
    
    print("\n¿Qué desea actualizar?")
    print("1. Nombre")
    print("2. Email")
    print("3. Teléfono")
    print("4. Actualizar todo")
    
    option = input("\nSeleccione una opción: ").strip()
    
    try:
        if option == "1":
            new_name = input("Nuevo nombre: ").strip()
            if new_name:
                user.name = new_name
        
        elif option == "2":
            new_email = input("Nuevo email: ").strip()
            user.email = new_email if new_email else None
        
        elif option == "3":
            new_phone = input("Nuevo teléfono: ").strip()
            user.phone = new_phone if new_phone else None
        
        elif option == "4":
            new_name = input("Nuevo nombre: ").strip()
            new_email = input("Nuevo email (opcional): ").strip()
            new_phone = input("Nuevo teléfono (opcional): ").strip()
            
            if new_name:
                user.name = new_name
                user.email = new_email if new_email else None
                user.phone = new_phone if new_phone else None
        
        else:
            print("\n❌ Opción no válida")
            return
        
        result = service_update_user(user)
        
        if result:
            print("\n✅ Usuario actualizado exitosamente")
            print_user(result)
        else:
            print("\n❌ No se pudo actualizar el usuario")
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def delete_user():
    """Opción 5: Eliminar usuario"""
    print_header("ELIMINAR USUARIO")
    
    user_id = input("\nIngrese ID del usuario a eliminar: ").strip()
    user = service_get_user_by_id(user_id)
    
    if not user:
        print(f"\n❌ No se encontró ningún usuario con el ID: {user_id}")
        return
    
    print("\n👤 Usuario a eliminar:")
    print_user(user)
    
    # Verificar si tiene préstamos activos
    if user.has_active_loans():
        print(f"\n⚠️  ADVERTENCIA: Este usuario tiene {len(user.loans)} préstamo(s) activo(s)")
        print("   No se recomienda eliminar usuarios con préstamos pendientes")
        print("   Considere devolver los préstamos primero")
    
    confirm = input("\n⚠️  ¿Está seguro de eliminar este usuario? (s/n): ").strip().lower()
    
    if confirm == "s":
        result = service_delete_user(user_id)
        if result:
            print("\n✅ Usuario eliminado exitosamente")
        else:
            print("\n❌ No se pudo eliminar el usuario")
    else:
        print("\n❌ Operación cancelada")


def view_users_with_loans():
    """Opción 6: Ver usuarios con préstamos activos"""
    print_header("USUARIOS CON PRÉSTAMOS ACTIVOS")
    
    users = service_get_users_with_active_loans()
    
    if not users:
        print("\n✅ No hay usuarios con préstamos activos")
        return
    
    print(f"\nTotal de usuarios con préstamos: {len(users)}")
    
    for i, user in enumerate(users):
        print_user(user, i)
        
        # Mostrar detalles de los préstamos
        loans = service_get_loans_by_user(user.id)
        active_loans = [loan for loan in loans if not loan.returned]
        
        if active_loans:
            print(f"\n   📚 Libros prestados:")
            for loan in active_loans:
                status = "⚠️ VENCIDO" if loan.is_overdue() else "✅ Activo"
                print(f"      • {loan.book.title} - {status}")
                print(f"        Vence: {loan.expiration_date.strftime('%Y-%m-%d')}")


def view_user_detail():
    """Opción 7: Ver detalle completo de un usuario"""
    print_header("DETALLE DE USUARIO")
    
    user_id = input("\nIngrese ID del usuario: ").strip()
    user = service_get_user_by_id(user_id)
    
    if not user:
        print(f"\n❌ No se encontró ningún usuario con el ID: {user_id}")
        return
    
    print("\n👤 Información del usuario:")
    print(f"\n   ID: {user.id}")
    print(f"   Nombre: {user.name}")
    print(f"   Email: {user.email if user.email else 'No registrado'}")
    print(f"   Teléfono: {user.phone if user.phone else 'No registrado'}")
    
    # Obtener todos los préstamos del usuario
    loans = service_get_loans_by_user(user_id)
    
    if not loans:
        print(f"\n   Préstamos: Este usuario no tiene préstamos registrados")
        return
    
    # Separar préstamos activos y devueltos
    active_loans = [loan for loan in loans if not loan.returned]
    returned_loans = [loan for loan in loans if loan.returned]
    
    print(f"\n📊 Historial de préstamos:")
    print(f"   Total: {len(loans)}")
    print(f"   Activos: {len(active_loans)}")
    print(f"   Devueltos: {len(returned_loans)}")
    
    # Mostrar préstamos activos
    if active_loans:
        print(f"\n📚 Préstamos activos ({len(active_loans)}):")
        for i, loan in enumerate(active_loans):
            status = "⚠️ VENCIDO" if loan.is_overdue() else "✅ Activo"
            print(f"\n   [{i + 1}] {loan.book.title}")
            print(f"       Prestado: {loan.loan_date.strftime('%Y-%m-%d')}")
            print(f"       Vence: {loan.expiration_date.strftime('%Y-%m-%d')}")
            print(f"       Estado: {status}")
            if loan.is_overdue():
                print(f"       Días de retraso: {loan.days_overdue()}")
    
    # Mostrar préstamos devueltos (solo los últimos 5)
    if returned_loans:
        print(f"\n📦 Préstamos devueltos (últimos 5):")
        for i, loan in enumerate(returned_loans[-5:]):
            print(f"\n   [{i + 1}] {loan.book.title}")
            print(f"       Prestado: {loan.loan_date.strftime('%Y-%m-%d')}")
            print(f"       Devuelto: {loan.return_date.strftime('%Y-%m-%d')}")


def view_user_statistics():
    """Opción 8: Ver estadísticas de usuarios"""
    print_header("ESTADÍSTICAS DE USUARIOS")
    
    stats = service_get_user_statistics()
    
    print(f"\n📊 Resumen de usuarios:")
    print(f"\n   Total de usuarios registrados: {stats['total_users']}")
    print(f"   Usuarios con préstamos activos: {stats['users_with_active_loans']}")
    print(f"   Usuarios sin préstamos: {stats['users_without_loans']}")
    print(f"   Total de préstamos activos: {stats['total_active_loans']}")
    
    if stats['total_users'] > 0:
        percentage = (stats['users_with_active_loans'] / stats['total_users']) * 100
        print(f"\n   Porcentaje de usuarios activos: {percentage:.1f}%")
        
        if stats['users_with_active_loans'] > 0:
            avg_loans = stats['total_active_loans'] / stats['users_with_active_loans']
            print(f"   Promedio de préstamos por usuario activo: {avg_loans:.1f}")


def show_menu():
    """Muestra el menú principal de usuarios"""
    print_header("SISTEMA DE GESTIÓN DE USUARIOS")
    print("\n1. Agregar nuevo usuario")
    print("2. Listar todos los usuarios")
    print("3. Buscar usuario")
    print("4. Actualizar información de usuario")
    print("5. Eliminar usuario")
    print("6. Ver usuarios con préstamos activos")
    print("7. Ver detalle completo de usuario")
    print("8. Ver estadísticas de usuarios")
    print("0. Salir")


def user_menu():
    """Función principal del menú de usuarios"""
    while True:
        clear_screen()
        show_menu()
        
        option = input("\nSeleccione una opción: ").strip()
        
        if option == "1":
            add_user()
        elif option == "2":
            list_all_users()
        elif option == "3":
            search_user()
        elif option == "4":
            update_user_info()
        elif option == "5":
            delete_user()
        elif option == "6":
            view_users_with_loans()
        elif option == "7":
            view_user_detail()
        elif option == "8":
            view_user_statistics()
        elif option == "0":
            print("\n👋 Regresando al menú principal...")
            break
        else:
            print("\n❌ Opción no válida. Por favor, seleccione una opción del menú.")
        
        pause()


if __name__ == "__main__":
    user_menu()