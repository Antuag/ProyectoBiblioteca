from models.user import User
from pathlib import Path
import json


# Ruta segura (independiente del lugar donde ejecutes el programa)
ruta = Path(__file__).resolve().parent.parent / "data" / "users.json"


def _load_users():
    """Función auxiliar para cargar los usuarios desde el archivo JSON"""
    if ruta.is_file():
        try:
            with open(ruta, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def _save_users(users_list):
    """Función auxiliar para guardar los usuarios en el archivo JSON"""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as file:
        json.dump(users_list, file, indent=4, ensure_ascii=False)


def _user_to_dict(user: User):
    """Convierte un objeto User a diccionario"""
    return user.to_dict()


def _dict_to_user(user_dict):
    """Convierte un diccionario a objeto User"""
    user = User(
        id=user_dict["id"],
        name=user_dict["name"],
        email=user_dict.get("email"),
        phone=user_dict.get("phone"),
        loans=user_dict.get("loans", [])
    )
    return user


def create_user(user: User):
    """
    Crea un nuevo usuario.
    Si ya existe un usuario con el mismo ID, no lo crea y retorna None.
    """
    if not isinstance(user, User):
        raise TypeError("Debe ser un objeto de tipo User")
    
    users_list = _load_users()
    
    # Verificar si ya existe un usuario con ese ID
    for existing_user in users_list:
        if existing_user["id"] == user.id:
            print(f"Ya existe un usuario con el ID: {user.id}")
            return None
    
    # Convertir el User a diccionario y agregarlo
    user_dict = _user_to_dict(user)
    users_list.append(user_dict)
    
    # Guardar archivo
    _save_users(users_list)
    
    return user


def update_user(user: User):
    """
    Actualiza un usuario existente por su ID.
    Si no existe, retorna None.
    """
    if not isinstance(user, User):
        raise TypeError("Debe ser un objeto de tipo User")
    
    users_list = _load_users()
    
    # Buscar y actualizar el usuario
    for i, existing_user in enumerate(users_list):
        if existing_user["id"] == user.id:
            users_list[i] = _user_to_dict(user)
            _save_users(users_list)
            return user
    
    print(f"No se encontró un usuario con el ID: {user.id}")
    return None


def create_or_update_user(user: User):
    """
    Crea un nuevo usuario o actualiza uno existente.
    """
    if not isinstance(user, User):
        raise TypeError("Debe ser un objeto de tipo User")
    
    users_list = _load_users()
    
    # Buscar si ya existe
    for i, existing_user in enumerate(users_list):
        if existing_user["id"] == user.id:
            # Actualizar
            users_list[i] = _user_to_dict(user)
            _save_users(users_list)
            return user
    
    # Si no existe, crear
    user_dict = _user_to_dict(user)
    users_list.append(user_dict)
    _save_users(users_list)
    
    return user


def get_all_users():
    """
    Obtiene todos los usuarios.
    Retorna una lista de objetos User.
    """
    users_list = _load_users()
    return [_dict_to_user(user_dict) for user_dict in users_list]


def get_user_by_id(user_id):
    """
    Obtiene un usuario específico por su ID.
    Retorna un objeto User o None si no existe.
    """
    users_list = _load_users()
    
    for user_dict in users_list:
        if user_dict["id"] == user_id:
            return _dict_to_user(user_dict)
    
    return None


def delete_user(user_id):
    """
    Elimina un usuario por su ID.
    Retorna True si se eliminó, False si no se encontró.
    """
    users_list = _load_users()
    
    # Filtrar para eliminar el usuario con ese ID
    new_users_list = [user for user in users_list if user["id"] != user_id]
    
    if len(new_users_list) == len(users_list):
        print(f"No se encontró un usuario con el ID: {user_id}")
        return False
    
    _save_users(new_users_list)
    return True


def search_users_by_name(name):
    """
    Busca usuarios por nombre (búsqueda parcial, no case-sensitive).
    Retorna una lista de objetos User que coinciden.
    """
    users_list = _load_users()
    matching_users = []
    
    name_lower = name.lower()
    for user_dict in users_list:
        if name_lower in user_dict["name"].lower():
            matching_users.append(_dict_to_user(user_dict))
    
    return matching_users


def get_users_with_active_loans():
    """
    Obtiene todos los usuarios que tienen préstamos activos.
    Retorna una lista de objetos User.
    """
    users_list = _load_users()
    users_with_loans = []
    
    for user_dict in users_list:
        if user_dict.get("loans") and len(user_dict["loans"]) > 0:
            users_with_loans.append(_dict_to_user(user_dict))
    
    return users_with_loans


def get_user_statistics():
    """
    Obtiene estadísticas de usuarios.
    Retorna un diccionario con información resumida.
    """
    users_list = _load_users()
    
    total_users = len(users_list)
    users_with_loans = sum(1 for user in users_list if user.get("loans") and len(user["loans"]) > 0)
    total_active_loans = sum(len(user.get("loans", [])) for user in users_list)
    
    return {
        "total_users": total_users,
        "users_with_active_loans": users_with_loans,
        "users_without_loans": total_users - users_with_loans,
        "total_active_loans": total_active_loans
    }