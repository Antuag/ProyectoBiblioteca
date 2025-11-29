from persistence.fileManagment import *
from services.userManager import *
json = [
    {"id": "1055", "nombre": "andres", "edad": "19"},
    {"id": "1000", "nombre": "Juan", "edad": "19"},
    {"id": "5322123", "nombre": "Carlos", "edad": "19"},
    {"id": "30337212", "nombre": "Maria", "edad": "19"}
]

deletingUserId("1055")
countingUsers()