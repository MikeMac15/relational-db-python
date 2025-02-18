import os
import json
from pathlib import Path
from classes.field_class import Field

def read_schema(table_name:str):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    SCHEMA_DIR = BASE_DIR / 'schemas'
    schema_file = os.path.join(SCHEMA_DIR, f"{table_name}.schema.json")

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