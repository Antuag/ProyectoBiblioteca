from models.loan import Loan
class User:
    
    def __init__(self,id,name,loans=None):
        self.id=id
        self.name=name
        self.loans= list(loans) if loans is not None else []
    
    def adding_loans(self,loan: Loan):
        self.loans.append(Loan)
    
    def eliminating_loan(self,loan_id):
        self.loans=[loan for loan in self.loans if loan.id !=loan_id]

    def toJSON(self):
        user={
            "id":self.id,
            "name":self.name,
            "loans":self.loans if self.loans is not None else []
        }
        return user