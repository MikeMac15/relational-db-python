import os
import json
from pathlib import Path
from my_db.classes.field_class import Field
from my_db.helpers.get_db_files import get_schema_file

def read_schema(table_name:str):
    '''
    
    '''
    schema_file = get_schema_file(table_name)
    print(schema_file)
    try:
        with open(schema_file,'r') as file:
            schema = json.load(file)
            fields = [Field(**field) for field in schema["fields"]]
            return schema["table_name"], fields
    

    except FileNotFoundError:
        print("file not found: read_schema.py")
        return None,None
    except Exception as e:
        print('read_schema.py',e)
        return None,None