def insertion_sort_books_by_isbn(books):
    """
    Ordena una lista de diccionarios de libros por ISBN usando Insertion Sort.
    Modifica la lista en el mismo lugar (in-place).
    """

    for i in range(1, len(books)):
        key = books[i]                 # diccionario del libro
        key_isbn = key["isbn"]

        j = i - 1

        # Desplazar los elementos mayores una posición a la derecha
        while j >= 0 and books[j]["isbn"] > key_isbn:
            books[j + 1] = books[j]
            j -= 1

        # Insertar el libro en la posición correcta
        books[j + 1] = key
