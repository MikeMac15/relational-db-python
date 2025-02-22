import os
from pathlib import Path
def get_db_idx_file(table_name)->tuple:
    '''
    returns tuple (db_file, idx_file)
    '''
    return (os.path.join(Path(__file__).resolve().parent.parent, 'databases', f"{table_name}.db"), os.path.join(Path(__file__).resolve().parent.parent, 'databases', f"{table_name}.idx"))
    
def get_schema_file(table_name)->str:
    return os.path.join(Path(__file__).resolve().parent.parent, 'schemas', f"{table_name}.schema.json")
    
