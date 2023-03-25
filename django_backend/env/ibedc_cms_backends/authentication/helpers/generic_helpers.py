import json
from datetime import datetime

def cleanup(Object):
    del Object

def convertToDict(string):
    return json.loads(string)

def convertToNone(string):
        if string == 'None':
            return None
        return string

def getnumberfromstring(str):
        import re
        new_string = str
        new_result = re.findall(r"[-+]?\d*\.\d+|\d+", new_string)
        print(new_result)
        return new_result
    
def returndatetime():
    now = datetime.now()
    #date format: yyyy-mm-dd: HH:MM:SS
    format = "%Y-%m-%d--%H:%M:%S"
    date1 = now.strftime(format)
    print("Formatted Date:", date1)
    
    return str(date1)