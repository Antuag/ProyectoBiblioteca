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
