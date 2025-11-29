def validatingObjectExists(data,key,value):
    exists=False
    for element in data:
        if element.get(key)==value:
            exits=True
            break
    return exists