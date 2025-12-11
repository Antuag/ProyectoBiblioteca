"""
Algoritmo de Backtracking para encontrar la combinación óptima de libros en una estantería
sin exceder el peso máximo y maximizando el valor total.
"""

from models.book import Book
from services.book_service import get_all_books

MAX_WEIGHT = 8.0  # kg

def optimal_shelf_backtracking(books, max_weight=MAX_WEIGHT):
    # Limitar a los primeros 10 libros para evitar combinaciones excesivas
    books = books[:10]
    n = len(books)
    best_value = 0
    best_combination = []
    soluciones_validas = []

    def backtrack(index, current_combination, current_weight, current_value):
        nonlocal best_value, best_combination
        if current_weight > max_weight:
            return
        if index == n:
            # Solo mostrar soluciones con al menos un libro
            if current_weight <= max_weight and len(current_combination) > 0:
                soluciones_validas.append((current_combination[:], current_weight, current_value))
                print(f"✔️ Solución válida: {[b.title for b in current_combination]} | Peso: {current_weight:.2f} kg | Valor: {current_value}")
            if current_value > best_value and len(current_combination) > 0:
                best_value = current_value
                best_combination = current_combination[:]
            return
        # Opción 1: incluir el libro actual
        book = books[index]
        backtrack(index + 1,
                  current_combination + [book],
                  current_weight + book.weight,
                  current_value + book.value)
        # Opción 2: no incluir el libro actual
        backtrack(index + 1,
                  current_combination,  
                  current_weight,
                  current_value)

    backtrack(0, [], 0, 0)
    print(f"\nMejor combinación encontrada:")
    print(f"Libros: {[b.title for b in best_combination]}")
    print(f"Valor total: ${best_value}")
    print(f"Peso total: {sum(b.weight for b in best_combination):.2f} kg")
    return best_combination, best_value


