"""
Linear Search Algorithms for Books
"""

def linear_search_books(books, title=None, author=None):
    result = []
    for book in books:
        matches = True
        if title:
            matches = matches and (title.lower() in book.title.lower())
        if author:
            matches = matches and (author.lower() in book.author.lower())
        if matches:
            result.append(book)
    return result
