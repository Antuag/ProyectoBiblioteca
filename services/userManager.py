from persistence.fileManagment import *
from models.user import *
from Utils.Utils import *
fileName="users.json"

def creatingUser(user_id,user_name,user_loans=None):
    
    data=loadingData(fileName)
    exists=validatingObjectExists(data,"id",user_id)
    userCreated=False
    
    if exists:
        print(f"User: {user_id} already exists")
    
    elif not exists:
        if user_loans==None:
            user_loans=[]
        
        newUser=User(user_id,user_name,user_loans).toJSON()   
        
        data.append(newUser)
        
        writingData(fileName, data)
        userCreated=True
    
    return userCreated
def findingUserById(id):
    
    data=loadingData(fileName)
      
    for index,user in enumerate(data):
        if user.get("id")==id:
            return index
    
    print(f"The user: {id} doesn't exist")
    return -1


def getAll():

    data=loadingData(fileName)
    print(f"User's list: ")

    for user in data:
        
        print(json.dumps(user,indent=4))

def updatingUser(id, field,newValue):
    
    data=loadingData(fileName)
    updatedSuccesfully=False
    userIndex=findingUserById(id)
    
    if  userIndex !=-1:
        
        data[userIndex][field]=newValue
        
        writingData(fileName,data)
        
        updatedSuccesfully=True
    
    return updatedSuccesfully

def deletingUserId(id):
    
    data=loadingData(fileName)
    
    userIndex=findingUserById(id)
    if userIndex !=-1:
        deletedUser=data[userIndex]
        
        data.pop(userIndex)
        
        print(f"The user {deletedUser['nombre']}-{deletedUser['id']} was removed")
        
        writingData(fileName,data)

def countingUsers():
    data=loadingData(fileName)
    print(len(data))
    
        
