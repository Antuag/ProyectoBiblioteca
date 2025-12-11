def binary_search_isbn(books, isbn):
    left, right = 0, len(books) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if str(books[mid].isbn) == isbn:
            return books[mid] 
        elif str(books[mid].isbn) < isbn:
            left = mid + 1
        else:
            right = mid - 1
    
    return None