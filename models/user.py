class User:
    
    def __init__(self, id, name, email=None, phone=None, loans=None):
        """
        Inicializa un usuario
        
        Args:
            id: ID único del usuario
            name: Nombre del usuario
            email: Email del usuario (opcional)
            phone: Teléfono del usuario (opcional)
            loans: Lista de IDs de préstamos activos (opcional)
        """
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        # Guardar solo los IDs de los préstamos, no los objetos completos
        self.loans = list(loans) if loans is not None else []
    
    def add_loan(self, loan_id):
        """Agrega un ID de préstamo a la lista de préstamos del usuario"""
        if loan_id not in self.loans:
            self.loans.append(loan_id)
    
    def remove_loan(self, loan_id):
        """Elimina un ID de préstamo de la lista del usuario"""
        if loan_id in self.loans:
            self.loans.remove(loan_id)
    
    def has_active_loans(self):
        """Verifica si el usuario tiene préstamos activos"""
        return len(self.loans) > 0
    
    def can_borrow(self, max_loans=3):
        """Verifica si el usuario puede hacer más préstamos"""
        return len(self.loans) < max_loans
    
    def to_dict(self):
        """Convierte el usuario a diccionario para guardar en JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "loans": self.loans  # Lista de IDs de préstamos
        }
    
    def __str__(self):
        return f"Usuario [{self.id}] {self.name} - Préstamos activos: {len(self.loans)}"