from datetime import datetime
import uuid


class Loan:
    
    def __init__(self, book, user, loan_date, expiration_date, loan_id=None, returned=False, return_date=None):
        """
        Inicializa un préstamo
        
        Args:
            book: Objeto Book
            user: Objeto User
            loan_date: Fecha del préstamo (string formato "YYYY-MM-DD" o datetime)
            expiration_date: Fecha de vencimiento (string formato "YYYY-MM-DD" o datetime)
            loan_id: ID único del préstamo (se genera automáticamente si no se proporciona)
            returned: Si el préstamo fue devuelto
            return_date: Fecha de devolución (string formato "YYYY-MM-DD" o datetime)
        """
        self.loan_id = loan_id if loan_id else str(uuid.uuid4())
        self.book = book
        self.user = user
        
        # Convertir fechas a datetime si son strings
        if isinstance(loan_date, str):
            self.loan_date = datetime.strptime(loan_date, "%Y-%m-%d")
        else:
            self.loan_date = loan_date
            
        if isinstance(expiration_date, str):
            self.expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        else:
            self.expiration_date = expiration_date
        
        self.returned = returned
        
        # Convertir fecha de devolución si existe
        if return_date:
            if isinstance(return_date, str):
                self.return_date = datetime.strptime(return_date, "%Y-%m-%d")
            else:
                self.return_date = return_date
        else:
            self.return_date = None

    def is_overdue(self):
        """Verifica si el préstamo está vencido"""
        if self.returned:
            return False  # Si ya fue devuelto, no está vencido
        return datetime.now() > self.expiration_date
    
    def days_overdue(self):
        """Retorna cuántos días de retraso tiene el préstamo"""
        if not self.is_overdue():
            return 0
        delta = datetime.now() - self.expiration_date
        return delta.days
    
    def days_until_due(self):
        """Retorna cuántos días faltan para el vencimiento"""
        if self.returned:
            return 0
        delta = self.expiration_date - datetime.now()
        return delta.days if delta.days > 0 else 0
    
    def mark_as_returned(self, return_date=None):
        """Marca el préstamo como devuelto"""
        self.returned = True
        if return_date:
            if isinstance(return_date, str):
                self.return_date = datetime.strptime(return_date, "%Y-%m-%d")
            else:
                self.return_date = return_date
        else:
            self.return_date = datetime.now()
    
    def to_dict(self):
        """Convierte el préstamo a diccionario para guardar en JSON"""
        return {
            "loan_id": self.loan_id,
            "isbn": self.book.isbn,
            "book_title": self.book.title,  # Para facilitar la lectura
            "user_id": self.user.id,
            "user_name": self.user.name,  # Para facilitar la lectura
            "loan_date": self.loan_date.strftime("%Y-%m-%d"),
            "expiration_date": self.expiration_date.strftime("%Y-%m-%d"),
            "returned": self.returned,
            "return_date": self.return_date.strftime("%Y-%m-%d") if self.return_date else None
        }
    
    def __str__(self):
        status = "Devuelto" if self.returned else ("Vencido" if self.is_overdue() else "Activo")
        return (f"Préstamo [{self.loan_id[:8]}] - {self.book.title} prestado a {self.user.name} "
                f"| Vence: {self.expiration_date.strftime('%Y-%m-%d')} | Estado: {status}")