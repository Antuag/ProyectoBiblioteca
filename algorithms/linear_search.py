"""
Linear Search Algorithms for Books
----------------------------------
These functions implement classic linear search required by the project.
"""

def linear_search_books_by_title(books, title):
    result = []
    title = title.lower()

    for book in books:
        if title in book.title.lower():
            result.append(book)

    return result


def linear_search_books_by_author(books, author):
    result = []
    author = author.lower()

    for book in books:
        if author in book.author.lower():
            result.append(book)

    return result
