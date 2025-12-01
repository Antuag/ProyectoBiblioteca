"""
Inventory Manager
-----------------
This module acts as the main interface for managing and analyzing
the book inventory. It integrates:

- book_service (CRUD + persistence)
- algorithms (linear search, merge sort)
- models (Book objects)

It is the layer between controllers (menus) and services.
Controllers MUST call InventoryManager instead of book_service directly.
"""

from services.book_service import (
    get_all_books,
    get_book_by_isbn
)

from algorithms.linear_search import linear_search_books_by_title, linear_search_books_by_author
from algorithms.merge_sort import merge_sort_books_by_value


class InventoryManager:
    """
    Manager responsible for:
    - Searching books using classic algorithms
    - Sorting books using Merge Sort
    - Providing high-level inventory reports
    - Acting as the access point to book inventory logic
    """
    
    # ----------------------------------------------
    # BASIC GETTERS
    # ----------------------------------------------

    
    def get_books():
        """
        Returns all books as Book objects.
        """
        return get_all_books()

    
    def get_book(isbn: str):
        """
        Returns a single book by ISBN.
        """
        return get_book_by_isbn(isbn)

    # ----------------------------------------------
    # SEARCHING (LINEAR SEARCH ALGORITHMS)
    # ----------------------------------------------

    
    def search_by_title(title: str):
        """
        Returns a list of books whose title matches partially,
        using linear search algorithm.
        """
        books = get_all_books()
        return linear_search_books_by_title(books, title)

    
    def search_by_author(author: str):
        """
        Returns a list of books whose author matches partially,
        using linear search algorithm.
        """
        books = get_all_books()
        return linear_search_books_by_author(books, author)

    # ----------------------------------------------
    # SORTING (MERGE SORT)
    # ----------------------------------------------

    
    def sort_by_value():
        """
        Returns a new list of books sorted by value (ascending),
        using Merge Sort algorithm.
        """
        books = get_all_books()
        return merge_sort_books_by_value(books)

    # ----------------------------------------------
    # REPORTS
    # ----------------------------------------------

    
    def report_sorted_by_value():
        """
        Returns books sorted from lowest to highest value.
        """
        return InventoryManager.sort_by_value()

    
    def report_top_valuable(n=5):
        """
        Returns the top N most valuable books.
        """
        sorted_books = InventoryManager.sort_by_value()
        return sorted_books[-n:] if sorted_books else []

    
    def report_by_author(author: str):
        """
        Returns books from a specific author.
        """
        return InventoryManager.search_by_author(author)

    
    def report_inventory_summary():
        """
        Returns a general summary:
        - total books
        - total stock
        - most expensive book
        """
        books = get_all_books()

        if not books:
            return {
                "total_books": 0,
                "total_stock": 0,
                "most_expensive": None
            }

        total_stock = sum(b.stock for b in books)
        sorted_books = merge_sort_books_by_value(books)
        most_expensive = sorted_books[-1] if sorted_books else None

        return {
            "total_books": len(books),
            "total_stock": total_stock,
            "most_expensive": most_expensive.to_dict() if most_expensive else None
        }
