"""
Merge Sort Algorithm for Books
------------------------------
Sorts books by their value attribute.
"""

def merge_sort_books_by_value(books):
    if len(books) <= 1:
        return books

    mid = len(books) // 2
    left = merge_sort_books_by_value(books[:mid])
    right = merge_sort_books_by_value(books[mid:])

    return merge(left, right)


def merge(left, right):
    sorted_list = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i].value <= right[j].value:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])

    return sorted_list

def merge_sort_pairs(pairs):
    """
    Ordena una lista de pares (clave, objeto) usando merge sort.
    clave: cualquier valor comparable (ej: string)
    objeto: cualquier elemento asociado
    """
    if len(pairs) <= 1:
        return pairs

    mid = len(pairs) // 2
    left = merge_sort_pairs(pairs[:mid])
    right = merge_sort_pairs(pairs[mid:])

    return merge_pairs(left, right)


def merge_pairs(left, right):
    sorted_list = []
    i = j = 0

    while i < len(left) and j < len(right):
        # Compara por la clave (primer elemento del par)
        if left[i][0] <= right[j][0]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list
