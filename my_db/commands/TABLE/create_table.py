import json
import os
from pathlib import Path
from my_db.classes.field_class import Field

# nav out of commands dir to get to my_db
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCHEMA_DIR = BASE_DIR / 'schemas'
DB_DIR = BASE_DIR / 'databases'

def create_table(table_name:str , fields: list):
    '''
    initializes table by storing schema in empty .db file
    '''
    os.makedirs(SCHEMA_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)

    schema_file = os.path.join(SCHEMA_DIR, f"{table_name}.schema.json")
    db_file = os.path.join(DB_DIR, f"{table_name}.db")

    try:
        field_of_fields = []

        for x in fields:
            field_of_fields.append(x.to_dict())

        schema = {
            "table_name": table_name,
            "fields": field_of_fields
        }


        # create schema.json file
        with open(schema_file, 'w') as file:
            json.dump(schema,file,indent=4)

        # create empty db file
        with open(db_file, 'wb') as file:
            file.write(b"")
        
        return f'Table {table_name} created successfully.'
    
    except Exception as e:
        return f"An error occurred: {e}"
        