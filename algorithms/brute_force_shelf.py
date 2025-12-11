"""
Brute Force Shelf Algorithm (Manual Version)
--------------------------------------------
Generates all combinations of 4 books manually without itertools.
This is the pure brute-force version required in some assignments.
"""


def brute_force_shelf_manual(books, max_weight=8, size=4):
    """
    Manual brute force implementation that generates combinations
    of 4 books without using itertools.

    Args:
        books (list[Book]): inventory list
        max_weight (float): maximum allowed weight
        size (int): combination size (default 4)

    Returns:
        list[list[Book]]: valid combinations of books
    """

    n = len(books)
    valid_combinations = []

    # Nested loops implement brute force selection of 4 books
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for m in range(k + 1, n):

                    combo = [books[i], books[j], books[k], books[m]]
                    total = sum(b.weight for b in combo)

                    if total <= max_weight:
                        valid_combinations.append(combo)

    return valid_combinations
