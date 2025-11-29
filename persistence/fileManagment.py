import json
from pathlib import Path

def writingData(fileName, content):
    
    folder = Path("data")
    file_path = folder / fileName

    folder.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)

def loadingData(fileName):
    
    folder=Path("data")
    file_path= folder / fileName
    
    try:   
        
        with file_path.open("r",encoding="utf-8") as file:
            content=json.load(file)
            return content
        
    except FileNotFoundError:
        
        print(f"The file :{fileName} -> doesn't exists")
        return []
    except json.JSONDecodeError:
        print(f"The file : {fileName} -> is not valid JSON")
        return []


    
            