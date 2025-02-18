import struct
import os
from pathlib import Path
from my_db.commands.TABLE.utils.get_last_record_id import get_last_record_id
from my_db.commands.TABLE.utils.generate_binary_format import generate_binary_format
from my_db.commands.TABLE.read_schema import read_schema

def INSERT(values:dict, table_name:str) -> int:
    '''
    inserts new record into .db binary file
    '''
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DB_DIR = BASE_DIR / 'databases'
    db_file = os.path.join(DB_DIR, f"{table_name}.db")


    table_name, fields = read_schema(table_name)

    if not fields:
        print('not a valid schema: no fields found')
        return -1 # error code
    
    last_id = get_last_record_id(table_name)

    new_record = {}

    for field in fields:
        field_name = field.name

        if field_name == 'id' and field.unique:
            new_record[field_name] = last_id + 1
        
        if field_name in values:
            new_record[field_name] = values[field_name]
        elif field.default is not None:
            new_record[field_name] = field.default
        elif not field.nullable:
            print('Value cannot be nullable')
            return -1
        else:
            new_record[field_name] = None

        
        binary_format = generate_binary_format(fields)
        packed_data = []

        for field in fields:
            value = new_record[field.name]
            if field.type == 'int':
                packed_data.append(int(value))
            elif field.type == 'str':
                packed_data.append(value.encode("utf-8").ljust(field.max_size, b'\x00'))

            with open(db_file, 'ab') as file:
                file.write(struct.pack(binary_format, *packed_data))
            
            print(f'Record inserted successfully at row {new_record.id}')
            return new_record.id
        