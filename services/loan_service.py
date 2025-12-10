from models.loan import Loan
from services.book_service import update_stock
from pathlib import Path
import json
from datetime import datetime, timedelta
from services.history_service import push_history
from services.book_service import update_book


# Ruta segura (independiente del lugar donde ejecutes el programa)
ruta = Path(__file__).resolve().parent.parent / "data" / "loans.json"


def _load_loans():
    """Función auxiliar para cargar los préstamos desde el archivo JSON"""
    if ruta.is_file():
        try:
            with open(ruta, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def _save_loans(loans_list):
    """Función auxiliar para guardar los préstamos en el archivo JSON"""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as file:
        json.dump(loans_list, file, indent=4, ensure_ascii=False)


def _loan_to_dict(loan: Loan):
    """Convierte un objeto Loan a diccionario"""
    return loan.to_dict()


def _dict_to_loan(loan_dict):
    """Convierte un diccionario a objeto Loan"""
    # Necesitamos reconstruir los objetos Book y User
    from services.book_service import get_book_by_isbn
    from services.user_service import get_user_by_id
    
    book = get_book_by_isbn(loan_dict["isbn"])
    user = get_user_by_id(loan_dict["user_id"])
    
    if not book or not user:
        return None
    
    loan = Loan(
        book=book,
        user=user,
        loan_date=loan_dict["loan_date"],
        expiration_date=loan_dict["expiration_date"],
        loan_id=loan_dict["loan_id"],
        returned=loan_dict.get("returned", False),
        return_date=loan_dict.get("return_date")
    )
    
    return loan


def create_loan(isbn, user_id, days=14):
    """
    Crea un nuevo préstamo.
    
    Args:
        isbn: ISBN del libro a prestar
        user_id: ID del usuario que solicita el préstamo
        days: Días de duración del préstamo (por defecto 14)
    
    Returns:
        Loan object si se creó exitosamente, None en caso contrario
    """
    from services.book_service import get_book_by_isbn, update_stock
    from services.user_service import get_user_by_id, update_user
    
    # Verificar que el libro existe y tiene stock
    book = get_book_by_isbn(isbn)
    if not book:
        print(f"❌ No se encontró un libro con el ISBN: {isbn}")
        return None
    
    if not book.isAvalible():
        print("\n⚠️ Este libro no tiene stock.")

    # Si el libro NO tiene stock → agregar a cola del book
    if not book.isAvalible():

    # evitar duplicados
        for r in book.reservations.queue:
            if r["user_id"] == user_id:
                print("❌ Ya estás en la lista de espera.")
                return None

    # agregar a la cola interna del libro
        book.reservations.enqueue({
            "user_id": user_id,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

    # guardar en books.json
        update_book(book)

        print("📌 Se agregó el usuario a la lista de espera (cola FIFO).")
        return None
    
    
    # Verificar que el usuario existe
    user = get_user_by_id(user_id)
    if not user:
        print(f"❌ No se encontró un usuario con el ID: {user_id}")
        return None
    
    # Verificar límite de préstamos del usuario
    if not user.can_borrow():
        print(f"❌ El usuario '{user.name}' ha alcanzado el límite de préstamos activos")
        return None
    
    # Calcular fechas
    loan_date = datetime.now()
    expiration_date = loan_date + timedelta(days=days)
    
    # Crear el préstamo
    new_loan = Loan(
        book=book,
        user=user,
        loan_date=loan_date.strftime("%Y-%m-%d"),
        expiration_date=expiration_date.strftime("%Y-%m-%d")
    )
    
    # Guardar en JSON
    loans_list = _load_loans()
    loan_dict = _loan_to_dict(new_loan)
    loans_list.append(loan_dict)
    _save_loans(loans_list)
    
    # Actualizar stock del libro (restar 1)
    update_stock(isbn, -1)
    
    # Agregar préstamo al usuario
    user.add_loan(new_loan.loan_id)
    update_user(user)
    
    #historial en pila lifo
    push_history(user_id, isbn)
    
    return new_loan


def return_loan(loan_id):
    """
    Marca un préstamo como devuelto y aumenta el stock del libro.
    
    Args:
        loan_id: ID del préstamo a devolver
    
    Returns:
        Loan object si se devolvió exitosamente, None en caso contrario
    """
    from services.user_service import get_user_by_id, update_user
    
    loans_list = _load_loans()
    
    # Buscar el préstamo
    for i, loan_dict in enumerate(loans_list):
        if loan_dict["loan_id"] == loan_id:
            
            # Verificar que no esté ya devuelto
            if loan_dict.get("returned", False):
                print(f"❌ Este préstamo ya fue devuelto anteriormente")
                return None
            
            # Marcar como devuelto
            loan_dict["returned"] = True
            loan_dict["return_date"] = datetime.now().strftime("%Y-%m-%d")
            
            # Guardar cambios
            loans_list[i] = loan_dict
            _save_loans(loans_list)
            
            # Aumentar stock del libro
            update_stock(loan_dict["isbn"], 1)
            
            # ¿Hay reservas?
            next_user = dequeue_reservation(loan_dict["isbn"])

            if next_user:
                print("\n📌 Este libro tenía una reserva.")
                print(f"   Usuario en turno: {next_user['user_id']}")

            # Crear préstamo automático
                from services.loan_service import create_loan
                auto_loan = create_loan(loan_dict["isbn"], next_user["user_id"])

                if auto_loan:
                    print("✔ Se creó el préstamo automáticamente para el siguiente usuario en la cola.")
            
            # Remover préstamo del usuario
            user = get_user_by_id(loan_dict["user_id"])
            if user:
                user.remove_loan(loan_id)
                update_user(user)
            
            # Retornar el préstamo actualizado
            return _dict_to_loan(loan_dict)
    
    print(f"❌ No se encontró un préstamo con el ID: {loan_id}")
    return None


def get_all_loans():
    """
    Obtiene todos los préstamos.
    Retorna una lista de objetos Loan.
    """
    loans_list = _load_loans()
    loans = []
    
    for loan_dict in loans_list:
        loan = _dict_to_loan(loan_dict)
        if loan:
            loans.append(loan)
    
    return loans


def get_active_loans():
    """
    Obtiene todos los préstamos activos (no devueltos).
    Retorna una lista de objetos Loan.
    """
    loans_list = _load_loans()
    active_loans = []
    
    for loan_dict in loans_list:
        if not loan_dict.get("returned", False):
            loan = _dict_to_loan(loan_dict)
            if loan:
                active_loans.append(loan)
    
    return active_loans


def get_overdue_loans():
    """
    Obtiene todos los préstamos vencidos.
    Retorna una lista de objetos Loan.
    """
    active_loans = get_active_loans()
    overdue_loans = [loan for loan in active_loans if loan.is_overdue()]
    return overdue_loans


def get_loans_by_user(user_id):
    """
    Obtiene todos los préstamos de un usuario específico.
    
    Args:
        user_id: ID del usuario
    
    Returns:
        Lista de objetos Loan
    """
    loans_list = _load_loans()
    user_loans = []
    
    for loan_dict in loans_list:
        if loan_dict["user_id"] == user_id:
            loan = _dict_to_loan(loan_dict)
            if loan:
                user_loans.append(loan)
    
    return user_loans


def get_loans_by_book(isbn):
    """
    Obtiene todos los préstamos de un libro específico.
    
    Args:
        isbn: ISBN del libro
    
    Returns:
        Lista de objetos Loan
    """
    loans_list = _load_loans()
    book_loans = []
    
    for loan_dict in loans_list:
        if loan_dict["isbn"] == isbn:
            loan = _dict_to_loan(loan_dict)
            if loan:
                book_loans.append(loan)
    
    return book_loans


def get_loan_by_id(loan_id):
    """
    Obtiene un préstamo específico por su ID.
    
    Args:
        loan_id: ID del préstamo
    
    Returns:
        Objeto Loan o None si no existe
    """
    loans_list = _load_loans()
    
    for loan_dict in loans_list:
        if loan_dict["loan_id"] == loan_id:
            return _dict_to_loan(loan_dict)
    
    return None


def delete_loan(loan_id):
    """
    Elimina un préstamo del sistema (solo usar para correcciones, no devuelve stock).
    
    Args:
        loan_id: ID del préstamo a eliminar
    
    Returns:
        True si se eliminó, False si no se encontró
    """
    loans_list = _load_loans()
    
    # Filtrar para eliminar el préstamo con ese ID
    new_loans_list = [loan for loan in loans_list if loan["loan_id"] != loan_id]
    
    if len(new_loans_list) == len(loans_list):
        print(f"❌ No se encontró un préstamo con el ID: {loan_id}")
        return False
    
    _save_loans(new_loans_list)
    return True


def get_loan_statistics():
    """
    Obtiene estadísticas de los préstamos.
    Retorna un diccionario con información resumida.
    """
    loans_list = _load_loans()
    
    total_loans = len(loans_list)
    active_loans = sum(1 for loan in loans_list if not loan.get("returned", False))
    returned_loans = total_loans - active_loans
    
    # Calcular préstamos vencidos
    overdue_count = 0
    for loan_dict in loans_list:
        if not loan_dict.get("returned", False):
            expiration = datetime.strptime(loan_dict["expiration_date"], "%Y-%m-%d")
            if datetime.now() > expiration:
                overdue_count += 1
    
    return {
        "total_loans": total_loans,
        "active_loans": active_loans,
        "returned_loans": returned_loans,
        "overdue_loans": overdue_count,
        "on_time_loans": active_loans - overdue_count
    }


def renew_loan(loan_id, additional_days=14):
    """
    Renueva un préstamo extendiendo su fecha de vencimiento.
    
    Args:
        loan_id: ID del préstamo a renovar
        additional_days: Días adicionales a agregar
    
    Returns:
        Loan object si se renovó exitosamente, None en caso contrario
    """
    loans_list = _load_loans()
    
    for i, loan_dict in enumerate(loans_list):
        if loan_dict["loan_id"] == loan_id:
            
            # Verificar que no esté devuelto
            if loan_dict.get("returned", False):
                print(f"❌ No se puede renovar un préstamo ya devuelto")
                return None
            
            # Extender fecha de vencimiento
            current_expiration = datetime.strptime(loan_dict["expiration_date"], "%Y-%m-%d")
            new_expiration = current_expiration + timedelta(days=additional_days)
            loan_dict["expiration_date"] = new_expiration.strftime("%Y-%m-%d")
            
            # Guardar cambios
            loans_list[i] = loan_dict
            _save_loans(loans_list)
            
            return _dict_to_loan(loan_dict)
    
    print(f"❌ No se encontró un préstamo con el ID: {loan_id}")
    return None