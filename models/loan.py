from structures.stack import Stack
from datetime import datetime

class Loan:
    
    def __init__(self,book,user, loanDate, expirationDate):
        
        self.book = book
        self.user = user
        self.loanDate = datetime.strptime(loanDate, "%Y-%m-%d")
        self.expirationDate = datetime.strptime(expirationDate, "%Y-%m-%d")

    def isOverdue(self):
        return datetime.now() > self.expirationDate
    
    def toDict(self):
        return {
        "isbn": self.book.isbn,   
        "userId": self.user.id,   
        "loanDate": self.loanDate_str,   
        "expirationDate": self.expirationDate_str,  
    }