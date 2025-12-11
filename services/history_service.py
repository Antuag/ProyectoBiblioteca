from pathlib import Path
import json
from datetime import datetime
from structures.stack import Stack

HISTORY_PATH = Path(__file__).resolve().parent.parent / "data" / "history.json"


def _load_history():
    """Carga el archivo completo de historial (por usuario)."""
    if HISTORY_PATH.is_file():
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def _save_history(history):
    """Guarda el historial completo."""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def push_history(user_id, isbn):
    """
    Inserta un nuevo registro en la Pila del usuario.
    Estructura LIFO.
    """
    history = _load_history()

    # Crear la pila si no existe
    if user_id not in history:
        history[user_id] = []

    entry = {
        "isbn": isbn,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    # Insertar al final → LIFO
    history[user_id].append(entry)

    _save_history(history)

def get_user_history_stack(user_id):
    """
    Carga el historial del usuario como una Pila real.
    """
    history = _load_history()

    stack = Stack()

    if user_id not in history:
        return stack  # Pila vacía

    for entry in history[user_id]:
        stack.push(entry)

    return stack
