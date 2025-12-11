"""
Funciones recursivas usadas en los reportes.
"""


def recursive_show_stack(stack):
    """Imprime una pila usando recursión sin destruir sus datos."""
    if stack.is_empty():
        return

    item = stack.pop()
    print(f"- {item}")

    recursive_show_stack(stack)

    stack.push(item)
    


def recursive_show_queue(queue):
    """Imprime una cola usando recursión sin destruir sus datos."""
    if queue.is_empty():
        return

    item = queue.dequeue()
    print(f"- {item}")

    recursive_show_queue(queue)

    queue.enqueue(item)
# --- NUEVAS FUNCIONES RECURSIVAS PARA REPORTES POR AUTOR ---

def recursive_total_value_by_author(books, author, index=0):
    """
    Recursión de pila:
    Calcula el valor total de todos los libros de un autor específico.

    Cada llamada espera el resultado de la siguiente (acumulación por return),
    por eso es un ejemplo clásico de recursión de pila.
    """
    if index == len(books):
        return 0

    book = books[index]
    current_value = book.value if book.author.lower() == author.lower() else 0

    # La suma se arma al “regresar” por la pila de llamadas
    return current_value + recursive_total_value_by_author(books, author, index + 1)


def _tail_recursive_weight_acc(books, author, index=0, total_weight=0.0, count=0):
    """
    Función auxiliar de recursión de cola.
    Acumula peso total y cantidad de libros del autor.
    """
    if index == len(books):
        return total_weight, count

    book = books[index]
    if book.author.lower() == author.lower():
        total_weight += book.weight
        count += 1

    # Mensaje para demostrar la lógica de la recursión de cola por consola
    print(f"[TAIL] index={index}, peso_acumulado={total_weight:.2f}, cantidad={count}")

    # La llamada recursiva es la ÚLTIMA operación -> recursión de cola
    return _tail_recursive_weight_acc(books, author, index + 1, total_weight, count)


def tail_recursive_average_weight_by_author(books, author):
    """
    Recursión de cola:
    Calcula el peso promedio de la colección de un autor.
    Usa _tail_recursive_weight_acc como acumulador.
    """
    total_weight, count = _tail_recursive_weight_acc(books, author)

    if count == 0:
        return 0.0

    return total_weight / count

